# AtmoSync – IoT Container Monitoring
## Snowflake Data Engineering Module
This module stores and processes IoT container sensor data using Snowflake.
### Architecture
Python Sensor Simulator → Kafka Producer → Kafka Topic → Python Kafka Consumer → Snowflake
### Snowflake Configuration
- Database: ATMOSYNC_DB
- Schema: RAW_DATA
- Warehouse: COMPUTE_WH
- Raw Table: CONTAINER_EVENTS_RAW
- Analytics View: CONTAINER_SENSOR_VIEW

### Folder Structure

```text
data_engineering/
└── snowflake/
    ├── consumer/
    │   └── kafka_to_snowflake.py
    └── sql/
        ├── 01_create_raw_table.sql
        └── 02_create_sensor_view.sql
```
### Data Flow
1. Python simulator generates container sensor events.
2. Kafka producer publishes events to `atmosync-sensor-data`.
3. Python consumer reads JSON messages.
4. Snowflake stores raw JSON payloads in `CONTAINER_EVENTS_RAW`.
5. `CONTAINER_SENSOR_VIEW` extracts structured sensor columns for analytics.
### Setup Requirements
- Python 3
- Apache Kafka
- Snowflake account
- Required Python packages:
  - kafka-python
  - snowflake-connector-python
  - python-dotenv
### Security

Snowflake credentials must be stored in a local `.env` file and must never be committed to GitHub.

