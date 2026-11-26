
import json
import os
from kafka import KafkaConsumer
import snowflake.connector
from dotenv import load_dotenv

# Load Snowflake credentials
load_dotenv(os.path.expanduser("~/atmosync/.env"))

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")

if not all([SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT]):
    raise ValueError("Missing Snowflake credentials in .env file")

# Connect to Kafka using a separate test consumer group
consumer = KafkaConsumer(
    "atmosync-sensor-data",
    bootstrap_servers="localhost:9092",
    group_id="atmosync-avocado-test-consumer",
    auto_offset_reset="latest",
    enable_auto_commit=False,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

# Connect specifically to the avocado test table's schema
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

print("Connected to Kafka and Snowflake avocado test consumer!")

try:
    for message in consumer:
        data = message.value

        # Accept only avocado events
        if data.get("commodity", "").strip().lower() != "avocados":
            print(f"Skipped non-avocado event: {data.get('event_id')}")
            consumer.commit()
            continue

        cursor.execute(
            """
            MERGE INTO CONTAINER_EVENTS_RAW_AVOCADO_TEST AS target
            USING (
                SELECT %s AS EVENT_ID, PARSE_JSON(%s) AS RAW_PAYLOAD
            ) AS source
            ON target.EVENT_ID = source.EVENT_ID
            WHEN NOT MATCHED THEN
                INSERT (EVENT_ID, RAW_PAYLOAD)
                VALUES (source.EVENT_ID, source.RAW_PAYLOAD)
            """,
            (data["event_id"], json.dumps(data))
        )

        consumer.commit()
        print(f"Avocado event stored: {data['event_id']}")

except KeyboardInterrupt:
    print("Avocado test consumer stopped.")

finally:
    consumer.close()
    cursor.close()
    conn.close()

