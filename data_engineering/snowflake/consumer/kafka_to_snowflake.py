
import json
import os
from kafka import KafkaConsumer
import snowflake.connector
from dotenv import load_dotenv

# Load private credentials from .env
load_dotenv()

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")

if not all([SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT]):
    raise ValueError("Missing Snowflake credentials in .env file")

# Connect to Kafka
consumer = KafkaConsumer(
    "atmosync-sensor-data",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

# Connect to Snowflake
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

print("Connected to Kafka and Snowflake!")

try:
    for message in consumer:
        data = message.value

        cursor.execute(
            """
            INSERT INTO CONTAINER_EVENTS_RAW
            (EVENT_ID, RAW_PAYLOAD)
            SELECT %s, PARSE_JSON(%s)
            """,
            (
                data["container_id"] + "_" + data["timestamp"],
                json.dumps(data)
            )
        )

        print("Inserted into Snowflake:", data)

except KeyboardInterrupt:
    print("Consumer stopped.")

finally:
    consumer.close()
    cursor.close()
    conn.close()

