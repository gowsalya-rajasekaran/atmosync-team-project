# AtmoSync – Data Dictionary

## 1. Overview

This document describes the four analytical datasets prepared for the
AtmoSync IoT Container Sensor Data Pipeline.

**Snowflake database:** ATMOSYNC_DB
**Snowflake schema:** RAW_DATA_ANALYTICS

These datasets are intended for reporting and visualization in Apache Superset.

## 2. Dataset Summary

| Dataset | Rows verified | Purpose |
|---|---:|---|
| MART_CONTAINER_SUMMARY | 3 | Container-level summary and cargo valuation |
| MART_SENSOR_MONITORING | 3 | Sensor monitoring and statistical analysis |
| MART_AVOCADO_COMMODITY_VALUE | 11 | Avocado event-level commodity valuation |
| MART_SENSOR_COMMODITY_VALUE | 11 | Event-level sensor and cargo valuation |

*Row counts reflect the validation performed on 26 November 2026 and may change
as new events are ingested.*

---

## 3. MART_CONTAINER_SUMMARY

**Purpose:** Provides one summary record per container, including sensor
statistics, latest reported quantity and estimated cargo value.

| Column | Data type | Description |
|---|---|---|
| CONTAINER_ID | TEXT | Unique container identifier |
| COMMODITY | TEXT | Commodity transported by the container |
| TOTAL_SENSOR_EVENTS | NUMBER | Total sensor events recorded for the container |
| LATEST_REPORTED_QUANTITY_KG | NUMBER | Latest reported cargo quantity in kilograms |
| AVG_TEMPERATURE | FLOAT | Average recorded temperature |
| AVG_HUMIDITY | FLOAT | Average recorded humidity |
| AVG_VIBRATION | FLOAT | Average recorded vibration |
| FIRST_EVENT_TIMESTAMP | TIMESTAMP_NTZ | Timestamp of the first recorded event |
| LATEST_EVENT_TIMESTAMP | TIMESTAMP_NTZ | Timestamp of the latest recorded event |
| PRICE_PER_KG | NUMBER | Commodity price per kilogram |
| ESTIMATED_CARGO_VALUE_INR | NUMBER | Estimated cargo value in Indian rupees |

**Recommended Superset visualizations:**
- KPI cards for total containers and sensor events
- Table showing container, commodity and cargo quantity
- Bar chart comparing estimated cargo value by container
- Container-level average sensor readings

---

## 4. MART_SENSOR_MONITORING

**Purpose:** Provides container-level minimum, average and maximum sensor
measurements for monitoring environmental conditions.

| Column | Data type | Description |
|---|---|---|
| CONTAINER_ID | TEXT | Unique container identifier |
| COMMODITY | TEXT | Commodity transported |
| TOTAL_SENSOR_EVENTS | NUMBER | Total sensor events used in the summary |
| MIN_TEMPERATURE | FLOAT | Minimum recorded temperature |
| AVG_TEMPERATURE | FLOAT | Average recorded temperature |
| MAX_TEMPERATURE | FLOAT | Maximum recorded temperature |
| MIN_HUMIDITY | FLOAT | Minimum recorded humidity |
| AVG_HUMIDITY | FLOAT | Average recorded humidity |
| MAX_HUMIDITY | FLOAT | Maximum recorded humidity |
| MAX_VIBRATION | FLOAT | Maximum recorded vibration |
| FIRST_EVENT_TIMESTAMP | TIMESTAMP_NTZ | Timestamp of the first recorded event |
| LATEST_EVENT_TIMESTAMP | TIMESTAMP_NTZ | Timestamp of the latest recorded event |

**Recommended Superset visualizations:**
- Temperature comparison chart using minimum, average and maximum values
- Humidity comparison chart
- Maximum vibration by container
- Container-level sensor monitoring table

---

## 5. MART_AVOCADO_COMMODITY_VALUE

**Purpose:** Provides event-level Avocado sensor information combined with
commodity pricing and calculated commodity value.

| Column | Data type | Description |
|---|---|---|
| EVENT_ID | TEXT | Unique sensor event identifier |
| EVENT_TIMESTAMP | TIMESTAMP_NTZ | Timestamp when the sensor event occurred |
| CONTAINER_ID | TEXT | Container identifier |
| COMMODITY | TEXT | Commodity name |
| QUANTITY_KG | NUMBER | Cargo quantity in kilograms |
| PRICE_PER_KG | NUMBER | Commodity price per kilogram |
| TOTAL_COMMODITY_VALUE | NUMBER | Calculated commodity value |
| TEMPERATURE | FLOAT | Temperature recorded in the event |
| HUMIDITY | FLOAT | Humidity recorded in the event |
| VIBRATION | FLOAT | Vibration recorded in the event |

**Recommended Superset visualizations:**
- Avocado cargo value by container
- Quantity comparison by container
- Event-level commodity valuation table
- Sensor readings alongside commodity value

---

## 6. MART_SENSOR_COMMODITY_VALUE

**Purpose:** Provides event-level cargo quantity, commodity pricing and
estimated cargo value for sensor events.

| Column | Data type | Description |
|---|---|---|
| EVENT_ID | TEXT | Unique sensor event identifier |
| EVENT_TIMESTAMP | TIMESTAMP_NTZ | Timestamp when the event occurred |
| CONTAINER_ID | TEXT | Container identifier |
| COMMODITY | TEXT | Commodity name |
| QUANTITY_KG | NUMBER | Cargo quantity in kilograms |
| PRICE_PER_KG | NUMBER | Commodity price per kilogram |
| ESTIMATED_CARGO_VALUE_INR | NUMBER | Estimated cargo value in Indian rupees |

**Recommended Superset visualizations:**
- Estimated cargo value by container
- Commodity value comparison
- Event-level cargo valuation table

---

## 7. Data Quality and Validation Notes

Validation performed on 26 November 2026:

| Check | Result |
|---|---:|
| Raw events | 56 |
| Unique raw event IDs | 56 |
| Raw events with NULL INGESTED_AT | 20 |
| Raw events with valid INGESTED_AT | 36 |
| Avocado raw events | 11 |
| Avocado staging events | 11 |
| Unique staging event IDs | 11 |
| Staging NULL EVENT_ID | 0 |
| Staging NULL EVENT_TIMESTAMP | 0 |
| Staging NULL INGESTED_AT | 10 |

The 20 raw records with NULL INGESTED_AT are historical records from before
the ingestion timestamp fix. The newer Kafka-to-Snowflake ingestion test
successfully stored an INGESTED_AT timestamp.

Historical ingestion timestamps have not been fabricated or backfilled.

The four mart datasets were successfully queried and their row counts verified.
The complete dbt build completed with 65 PASS, 0 WARN and 0 ERROR.

## 8. Important Limitations

- The four analytical marts do not currently contain latitude or longitude.
- Actual historical container routes cannot be plotted using these marts alone.
- Sensor temperature and humidity units should be confirmed against the
  simulator's source documentation before displaying units in dashboards.
- INGESTED_AT is available in the raw table but is not listed as a column in
  these four marts.
- The row counts represent the data available at validation time and can change.

## 9. Snowflake Dataset References

Use the following fully qualified table names in Superset:

- ATMOSYNC_DB.RAW_DATA_ANALYTICS.MART_CONTAINER_SUMMARY
- ATMOSYNC_DB.RAW_DATA_ANALYTICS.MART_SENSOR_MONITORING
- ATMOSYNC_DB.RAW_DATA_ANALYTICS.MART_AVOCADO_COMMODITY_VALUE
- ATMOSYNC_DB.RAW_DATA_ANALYTICS.MART_SENSOR_COMMODITY_VALUE
