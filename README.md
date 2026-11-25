# AtmoSync – IoT Container Monitoring

## Snowflake Data Engineering Module

AtmoSync is an IoT container monitoring data pipeline that collects container sensor events, streams them through Apache Kafka, stores them in Snowflake, and transforms them into analytical datasets using dbt.

## Architecture

Python Sensor Simulator → Kafka Producer → Kafka Topic → Python Kafka Consumer → Snowflake → dbt Transformations → Analytics Marts

## Snowflake Configuration

- **Database:** `ATMOSYNC_DB`
- **Schema:** `RAW_DATA`
- **Warehouse:** `COMPUTE_WH`
- **Raw Table:** `CONTAINER_EVENTS_RAW`
- **Analytics View:** `CONTAINER_SENSOR_VIEW`

### Additional Avocado Testing Objects

- `CONTAINER_EVENTS_RAW_AVOCADO_TEST`
- `CONTAINER_SENSOR_AVOCADO_TEST_VIEW`

These objects were created for isolated Avocado testing. The separate test table was empty during the latest validation.

## Folder Structure

```text
data_engineering/
└── snowflake/
    ├── consumer/
    │   └── kafka_to_snowflake.py
    └── sql/
        ├── 01_create_raw_table.sql
        └── 02_create_sensor_view.sql
```

The dbt project is maintained separately in the `atmosync_dbt/` directory.

## Data Flow

1. Python simulator generates container sensor events.
2. Kafka producer publishes events to the `atmosync-sensor-data` topic.
3. Python Kafka consumer reads JSON messages.
4. Snowflake stores raw JSON payloads in `CONTAINER_EVENTS_RAW`.
5. `CONTAINER_SENSOR_VIEW` extracts structured sensor columns.
6. dbt staging models clean, standardize and deduplicate sensor data.
7. dbt mart models prepare analytical datasets for reporting.

## Week 2 – Snowflake and dbt Implementation

### Staging Models

- `stg_container_sensors` – cleans and standardizes general container sensor data.
- `stg_avocado_sensors` – filters Avocado events, standardizes fields and removes duplicate events.

The Avocado staging model currently reads from the general `CONTAINER_SENSOR_VIEW` and filters for Avocado records.

### Mart Models

Four analytical mart models are implemented:

1. `mart_container_summary` – container-level summary, sensor averages and estimated cargo value.
2. `mart_avocado_commodity_value` – event-level Avocado commodity valuation.
3. `mart_sensor_commodity_value` – sensor event data enriched with commodity pricing.
4. `mart_sensor_monitoring` – aggregated sensor monitoring metrics.

### Commodity Pricing

- Seed file: `seeds/commodity_prices.csv`
- Commodity: Avocados
- Simulated price: ₹120 per kg

### Data Quality and Validation

dbt schema tests cover:
- Unique event identifiers.
- Non-null required fields.
- Accepted commodity values.
- Unique container and commodity combinations in summary models.

**Latest validation results:**

| Validation | Result |
|---|---:|
| Mart tests | 39 passed |
| Staging tests | 19 passed |
| Total dbt tests | 58 passed |
| Test errors | 0 |

The four mart models were also successfully rebuilt using dbt.

## Technologies

Python | Apache Kafka | Snowflake | dbt Core | SQL

## Security

Snowflake credentials must be stored in a local `.env` file and must never be committed to GitHub.
