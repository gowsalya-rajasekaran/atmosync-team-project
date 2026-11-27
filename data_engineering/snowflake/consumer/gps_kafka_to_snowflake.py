
import json
import os
import logging

from kafka import KafkaConsumer
import snowflake.connector
from dotenv import load_dotenv


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)
logger = logging.getLogger("atmosync_gps_consumer")


# Load Snowflake credentials
load_dotenv(os.path.expanduser("~/atmosync/.env"))

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")

if not all([SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT]):
    raise ValueError("Missing Snowflake credentials in .env")


# GPS Kafka configuration
GPS_TOPIC = "atmosync-gps-data"
BOOTSTRAP_SERVERS = ["localhost:9092"]

consumer = KafkaConsumer(
    GPS_TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    group_id="atmosync-gps-snowflake-consumer",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)


# Snowflake connection
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


def validate_gps_event(data):
    required_fields = {
        "event_id",
        "route_id",
        "leg_id",
        "container_id",
        "transport_mode",
        "latitude",
        "longitude",
        "speed_kmh",
        "heading",
        "location_timestamp"
    }

    if not isinstance(data, dict):
        raise ValueError("GPS event must be a JSON object")

    if set(data.keys()) != required_fields:
        raise ValueError("Missing or unexpected GPS fields")

    for field in [
        "event_id", "route_id", "leg_id",
        "container_id", "transport_mode",
        "location_timestamp"
    ]:
        if not isinstance(data[field], str) or not data[field].strip():
            raise ValueError(f"{field} must be a non-empty string")

    if data["transport_mode"] not in {"SEA", "ROAD"}:
        raise ValueError("Invalid transport mode")

    for field in ["latitude", "longitude", "speed_kmh", "heading"]:
        if isinstance(data[field], bool) or not isinstance(
            data[field], (int, float)
        ):
            raise ValueError(f"{field} must be numeric")

    if not -90 <= data["latitude"] <= 90:
        raise ValueError("Invalid latitude")

    if not -180 <= data["longitude"] <= 180:
        raise ValueError("Invalid longitude")

    if data["speed_kmh"] < 0:
        raise ValueError("Speed cannot be negative")

    if not 0 <= data["heading"] < 360:
        raise ValueError("Invalid heading")

    return True


logger.info("GPS consumer started. Waiting for GPS events...")

try:
    for message in consumer:
        data = message.value

        try:
            validate_gps_event(data)

            cursor.execute(
                """
                MERGE INTO CONTAINER_GPS_RAW AS target
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
                (data["event_id"], json.dumps(data))
            )

            # Commit offset only after Snowflake succeeds
            consumer.commit()

            logger.info(
                "GPS event stored and committed: %s",
                data["event_id"]
            )

        except Exception:
            logger.exception(
                "GPS processing failed. Offset not committed."
            )
            raise

except KeyboardInterrupt:
    logger.info("GPS consumer stopped.")

finally:
    consumer.close()
    cursor.close()
    conn.close()
    logger.info("GPS consumer connections closed.")
