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


---

## Week 2 – Snowflake and dbt Implementation

### Avocado Sensor Data Pipeline

An isolated avocado testing pipeline was prepared as part of the AtmoSync IoT Container Sensor Data Pipeline project.

### Snowflake Implementation
- Created a separate `CONTAINER_EVENTS_RAW_AVOCADO_TEST` table.
- Created `CONTAINER_SENSOR_AVOCADO_TEST_VIEW` to extract structured sensor fields from JSON payloads.
- Preserved the original raw sensor dataset.

### dbt Transformation
- Configured a separate avocado source in `sources.yml`.
- Developed `stg_avocado_sensors.sql` for data cleaning, duplicate removal and avocado filtering.
- Created `mart_avocado_commodity_value.sql` to combine sensor readings with commodity pricing.
- Added an isolated avocado pricing seed with a simulated price of 120 per kg.
- Configured data-quality tests for uniqueness, non-null values and accepted commodity values.

### Validation
- Successfully compiled and executed the avocado staging model.
- Successfully compiled and executed the commodity-value mart.
- Successfully executed 10 dbt data-quality tests.

### Current Status
Snowflake and dbt transformations are prepared and validated. Kafka producer integration and end-to-end data ingestion are pending.

### Technologies
Python | Apache Kafka | Snowflake | dbt Core | SQL
