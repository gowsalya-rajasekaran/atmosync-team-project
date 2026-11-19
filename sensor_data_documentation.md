# AtmoSync – Sensor Data Documentation

## 1. Project Overview
The AtmoSync Python Sensor Simulator generates simulated
telemetry data for cargo containers carrying perishable goods.

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
| CONT001 | Apples | 500 kg |
| CONT002 | Bananas | 700 kg |
| CONT003 | Mangoes | 400 kg |

## 4. Event Generation

- Generates a unique UUID for every event.
- Generates timestamps using UTC.
- Simulates temperature, humidity and vibration readings.
- Generates one event every 2 seconds.
- Runs continuously until stopped using Ctrl + C.

## 5. JSON Validation

Each event is checked for:
- Required fields.
- Correct data types.
- Valid JSON conversion.

## 6. Kafka Integration

Each sensor event is represented as one JSON object.
The JSON object can be sent as the value of a Kafka message.

The simulator currently prints one JSON event per line.

## 7. Notes

All readings are simulated for project testing.
Actual sensor ranges and vibration units should be
confirmed with the project team.