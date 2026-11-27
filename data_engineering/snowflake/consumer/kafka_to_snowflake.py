
import json
import os
import logging
from datetime import datetime, timezone

from kafka import KafkaConsumer, KafkaProducer
import snowflake.connector
from dotenv import load_dotenv


# --------------------------------------------------
# 1. Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

logger = logging.getLogger("atmosync_consumer")


# --------------------------------------------------
# 2. Configuration
# --------------------------------------------------

load_dotenv(os.path.expanduser("~/atmosync/.env"))

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")

if not all([SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT]):
    raise ValueError("Missing Snowflake credentials in .env file")

MAIN_TOPIC = os.getenv("KAFKA_INPUT_TOPIC", "atmosync-sensor-data")
DLQ_TOPIC = "atmosync-sensor-data-dlq"

BOOTSTRAP_SERVERS = ["localhost:9092"]

REQUIRED_FIELDS = {
    "event_id",
    "timestamp",
    "container_id",
    "temperature",
    "humidity",
    "vibration",
    "commodity",
    "quantity_kg"
}


# --------------------------------------------------
# 3. Kafka connections
# --------------------------------------------------

consumer = KafkaConsumer(
    MAIN_TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    group_id=os.getenv(
        "KAFKA_GROUP_ID",
        "atmosync-snowflake-consumer"
    ),
    auto_offset_reset=os.getenv("KAFKA_AUTO_OFFSET_RESET", "latest"),
    enable_auto_commit=False,
)

# Kafka producer for Dead Letter Queue
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

# --------------------------------------------------
# 4. Snowflake connection
# --------------------------------------------------
# --------------------------------------------------
# 4. Snowflake connection
# --------------------------------------------------

conn = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse="COMPUTE_WH",
    database="ATMOSYNC_DB",
    schema="RAW_DATA",
    role="ACCOUNTADMIN"
)

cursor = conn.cursor()

logger.info("Connected to Kafka and Snowflake!")


# --------------------------------------------------
# 5. Event validation
# --------------------------------------------------

def validate_event(data):

    if not isinstance(data, dict):
        raise ValueError("Event must be a JSON object")

    if set(data.keys()) != REQUIRED_FIELDS:
        raise ValueError("Missing or unexpected event fields")

    for field in [
        "event_id",
        "timestamp",
        "container_id",
        "commodity"
    ]:
        if not isinstance(data[field], str) or not data[field].strip():
            raise ValueError(f"{field} must be a non-empty string")

    for field in [
        "temperature",
        "humidity",
        "vibration",
        "quantity_kg"
    ]:
        if isinstance(data[field], bool) or not isinstance(
            data[field], (int, float)
        ):
            raise ValueError(f"{field} must be numeric")

    return True


# --------------------------------------------------
# 6. Dead Letter Queue
# --------------------------------------------------

def send_to_dlq(raw_message, error):

    dlq_record = {
        "original_message": raw_message.decode(
            "utf-8", errors="replace"
        ),
        "error": str(error),
        "failed_at": datetime.now(timezone.utc).isoformat(),
        "source_topic": MAIN_TOPIC
    }

    future = producer.send(DLQ_TOPIC, value=dlq_record)
    future.get(timeout=10)

    logger.error("Invalid event sent to DLQ: %s", error)


# --------------------------------------------------
# 7. Main consumer loop
# --------------------------------------------------

try:

    for message in consumer:

        raw_message = message.value

        try:

            # Parse JSON safely
            data = json.loads(raw_message.decode("utf-8"))

            # Validate event
            validate_event(data)

            # Insert into Snowflake without duplicates
            cursor.execute(
                """
                MERGE INTO CONTAINER_EVENTS_RAW AS target
                USING (
                    SELECT %s AS EVENT_ID, PARSE_JSON(%s) AS RAW_PAYLOAD
                ) AS source
                ON target.EVENT_ID = source.EVENT_ID
                WHEN NOT MATCHED THEN
                    INSERT (EVENT_ID, RAW_PAYLOAD, INGESTED_AT)
                    VALUES (
                        source.EVENT_ID,
                        source.RAW_PAYLOAD,
                        CURRENT_TIMESTAMP()
                    )
                """,
                (
                    data["event_id"],
                    json.dumps(data)
                )
            )

            # Commit Kafka offset only after Snowflake succeeds
            consumer.commit()

            logger.info(
                "Successfully stored and committed: %s",
                data["event_id"]
            )

        except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as error:

            # Send invalid messages to DLQ
            send_to_dlq(raw_message, error)

            # Commit only after DLQ publishing succeeds
            consumer.commit()

        except Exception:

            # Do not commit if Snowflake or another operation fails
            logger.exception(
                "Processing failed. Kafka offset not committed."
            )
            raise

except KeyboardInterrupt:
    logger.info("Consumer stopped.")

finally:

    try:
        consumer.close()
    finally:
        try:
            producer.close()
        finally:
            cursor.close()
            conn.close()
