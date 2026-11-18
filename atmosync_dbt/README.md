# AtmoSync – dbt Data Transformation Pipeline

## Project Overview

AtmoSync is an IoT-based container sensor data pipeline designed to process and analyze real-time container telemetry.

This dbt project transforms structured sensor data stored in Snowflake into clean, reliable, and analytics-ready datasets.

## Technology Stack

- **Data Warehouse:** Snowflake
- **Transformation Tool:** dbt Core
- **Adapter:** dbt-snowflake
- **Query Language:** SQL
- **Testing:** dbt data tests
- **Package:** dbt_utils

## Data Pipeline Architecture

The transformation workflow follows three main layers:

1. **Raw Layer:** Sensor events are stored in Snowflake.
2. **Staging Layer:** Data is cleaned, standardized, and deduplicated.
3. **Mart Layer:** Business-oriented summary and monitoring datasets are created.

## Project Models

### 1. Staging Model

**Model:** `stg_container_sensors`

Source:
`ATMOSYNC_DB.RAW_DATA.CONTAINER_SENSOR_VIEW`

Transformations:
- Trims unnecessary whitespace from identifiers.
- Standardizes commodity names using `INITCAP`.
- Removes duplicate events using `ROW_NUMBER()`.
- Retains the latest ingested record for each `EVENT_ID`.
- Filters records with missing event or container identifiers.

### 2. Mart Models

**Model: `mart_container_summary`**

Provides container-level summary metrics, including:
- Total sensor events.
- Latest reported quantity.
- Average temperature.
- Average humidity.
- Average vibration.
- First and latest event timestamps.

**Model: `mart_sensor_monitoring`**

Provides sensor monitoring metrics, including:
- Minimum, average, and maximum temperature.
- Minimum, average, and maximum humidity.
- Maximum vibration.
- Total sensor events.
- First and latest event timestamps.

Both mart models aggregate data by `CONTAINER_ID` and `COMMODITY`.

## Data Quality Testing

The project uses dbt data tests to validate data quality.

Tests include:
- `not_null` checks on required fields.
- `unique` validation for staging event IDs.
- Composite uniqueness checks for container and commodity combinations using `dbt_utils`.

### Latest Test Results

**28 tests passed successfully.**

- Staging: 9 tests
- Container Summary: 8 tests
- Sensor Monitoring: 11 tests
- Errors: 0

## Project Structure

```text
atmosync_dbt/
│
├── models/
│   ├── staging/
│   │   └── snowflake/
│   │       ├── sources.yml
│   │       ├── stg_container_sensors.sql
│   │       └── schema.yml
│   │
│   └── marts/
│       ├── mart_container_summary.sql
│       ├── mart_sensor_monitoring.sql
│       ├── schema.yml
│       └── mart_sensor_monitoring.yml
│
├── dbt_project.yml
├── packages.yml
└── README.md
```

## Running the Project

Activate the Python virtual environment and navigate to the dbt project directory.

Install dependencies:

```bash
dbt deps
```

Check the Snowflake connection:

```bash
dbt debug
```

Parse the project:

```bash
dbt parse
```

Run all models:

```bash
dbt run
```

Run all data quality tests:

```bash
dbt test
```

## Data Warehouse Configuration

- **Database:** `ATMOSYNC_DB`
- **Raw Schema:** `RAW_DATA`
- **Analytics Schema:** `RAW_DATA_ANALYTICS`

## Project Goal

The goal of this transformation layer is to convert raw IoT container sensor events into structured, tested, and analytics-ready datasets that support container-level analysis and sensor monitoring.