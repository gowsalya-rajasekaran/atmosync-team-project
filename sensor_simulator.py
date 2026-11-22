import json
import random
import time
import uuid
from datetime import datetime, timezone

# All containers carry mature-green Hass avocados.
CONTAINERS = {
    "CONT001": {"commodity": "Avocados", "quantity_kg": 500},
    "CONT002": {"commodity": "Avocados", "quantity_kg": 700},
    "CONT003": {"commodity": "Avocados", "quantity_kg": 400}
}

NORMAL_RANGES = {
    "temperature": (5, 7),
    "humidity": (90, 95)
}

ABNORMAL_RANGES = {
    "low_temperature": (2, 3.9),
    "high_temperature": (8.1, 10),
    "low_humidity": (80, 84.9),
    "high_humidity": (98.1, 100)
}

ABNORMAL_PROBABILITY = 0.10


def generate_sensor_event():
    container_id = random.choice(list(CONTAINERS.keys()))
    container = CONTAINERS[container_id]

    temperature = round(random.uniform(*NORMAL_RANGES["temperature"]), 2)
    humidity = round(random.uniform(*NORMAL_RANGES["humidity"]), 2)

    if random.random() < ABNORMAL_PROBABILITY:
        abnormal_type = random.choice([
            "low_temperature",
            "high_temperature",
            "low_humidity",
            "high_humidity"
        ])

        if abnormal_type == "low_temperature":
            temperature = round(random.uniform(*ABNORMAL_RANGES["low_temperature"]), 2)
        elif abnormal_type == "high_temperature":
            temperature = round(random.uniform(*ABNORMAL_RANGES["high_temperature"]), 2)
        elif abnormal_type == "low_humidity":
            humidity = round(random.uniform(*ABNORMAL_RANGES["low_humidity"]), 2)
        elif abnormal_type == "high_humidity":
            humidity = round(random.uniform(*ABNORMAL_RANGES["high_humidity"]), 2)

    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "container_id": container_id,
        "temperature": temperature,
        "humidity": humidity,
        "vibration": round(random.uniform(0.1, 1.0), 2),
        "commodity": container["commodity"],
        "quantity_kg": container["quantity_kg"]
    }

    return event


def validate_event(event):
    required_fields = {
        "event_id", "timestamp", "container_id",
        "temperature", "humidity", "vibration",
        "commodity", "quantity_kg"
    }

    if set(event.keys()) != required_fields:
        raise ValueError("Invalid JSON structure: incorrect fields")

    if not isinstance(event["event_id"], str):
        raise ValueError("event_id must be a string")

    if not isinstance(event["timestamp"], str):
        raise ValueError("timestamp must be a string")

    if not isinstance(event["container_id"], str):
        raise ValueError("container_id must be a string")

    if not isinstance(event["commodity"], str):
        raise ValueError("commodity must be a string")

    for field in ["temperature", "humidity", "vibration", "quantity_kg"]:
        if not isinstance(event[field], (int, float)):
            raise ValueError(f"{field} must be a number")

    json.loads(json.dumps(event))
    return True


if __name__ == "__main__":
    print("Starting AtmoSync Avocado Sensor Simulator...")
    print("Press Ctrl + C to stop.\n")

    try:
        while True:
            sensor_event = generate_sensor_event()

            if validate_event(sensor_event):
                print(json.dumps(sensor_event))

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nSensor simulation stopped.")
