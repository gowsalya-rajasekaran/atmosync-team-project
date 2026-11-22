# AtmoSync – Sensor Data Documentation

## 1. Project Overview

The AtmoSync Python Sensor Simulator generates simulated telemetry data for cargo containers carrying mature-green Hass avocados.

The simulator generates temperature, humidity, and vibration readings to help monitor the transportation conditions of avocado shipments.

## 2. Sensor Data Structure

| Field | Data Type | Description |
|---|---|---|
| event_id | String | Unique ID for every sensor event |
| timestamp | String | Event date and time in UTC |
| container_id | String | Unique cargo container ID |
| temperature | Float | Container temperature in Celsius |
| humidity | Float | Humidity level in percentage |
| vibration | Float | Simulated vibration reading |
| commodity | String | Type of goods being transported |
| quantity_kg | Integer | Quantity of goods in kilograms |

## 3. Container Details

| Container ID | Commodity | Quantity |
|---|---|---|
| CONT001 | Avocados | 500 kg |
| CONT002 | Avocados | 700 kg |
| CONT003 | Avocados | 400 kg |

All three containers are used for the mature-green Hass avocado shipment simulation.

## 4. Sensor Ranges and Event Generation

The simulator uses the following normal sensor ranges, as confirmed by the project team:

| Sensor | Normal Range | Abnormal Condition |
|---|---|---|
| Temperature | 5–7°C | Below 4°C or above 8°C |
| Humidity | 90–95% | Below 85% or above 98% |

- Approximately 90% of generated readings are normal.
- Approximately 10% of generated readings contain an abnormal temperature or humidity value.
- Both low and high abnormal readings are simulated.
- A unique UUID is generated for every event.
- Timestamps are generated using UTC.
- One event is generated every 2 seconds.
- The simulator runs continuously until stopped using Ctrl + C.

## 5. JSON Validation

Each generated event is checked for:

- Required fields.
- Correct data types.
- Valid JSON conversion.

The event structure remains consistent for downstream data processing.

## 6. Kafka and Snowflake Compatibility

Each sensor event is represented as one JSON object.

The JSON object can be sent as the value of a Kafka message.

The simulator prints one JSON event per line, making it suitable for streaming data pipelines and further processing for Snowflake.

The simulator generates data only and does not directly modify existing Snowflake records.

## 7. Notes

- All readings are simulated for project testing.
- Normal and abnormal sensor thresholds follow the values confirmed by the project team.
- The abnormal reading ranges are illustrative simulation values and can be adjusted later if required.
- Vibration readings are simulated values between 0.1 and 1.0; their units are not currently specified.
- Actual sensor readings and thresholds may differ from the simulated values.
-