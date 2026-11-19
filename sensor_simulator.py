import json
import random
import time
import uuid
from datetime import datetime, timezone

# Each container has a fixed commodity and quantity.
CONTAINERS = {
    "CONT001": {"commodity": "Apples", "quantity_kg": 500},
    "CONT002": {"commodity": "Bananas", "quantity_kg": 700},
    "CONT003": {"commodity": "Mangoes", "quantity_kg": 400}
}

# Illustrative temperature and humidity ranges for simulation.
COMMODITY_RANGES = {
    "Apples": {"temperature": (2, 8), "humidity": (85, 95)},
    "Bananas": {"temperature": (13, 15), "humidity": (85, 95)},
    "Mangoes": {"temperature": (10, 13), "humidity": (85, 90)}
}


def generate_sensor_event():
    container_id = random.choice(list(CONTAINERS.keys()))

    container = CONTAINERS[container_id]
    commodity = container["commodity"]
    ranges = COMMODITY_RANGES[commodity]

    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "container_id": container_id,
        "temperature": round(random.uniform(*ranges["temperature"]), 2),
        "humidity": round(random.uniform(*ranges["humidity"]), 2),
        "vibration": round(random.uniform(0.1, 1.0), 2),
        "commodity": commodity,
        "quantity_kg": container["quantity_kg"]
    }

    return event


def validate_event(event):
    required_fields = {
        "event_id", "timestamp", "container_id",
        "temperature", "humidity", "vibration",
        "commodity", "quantity_kg"
    }

    # Check that all required fields are present.
    if set(event.keys()) != required_fields:
        raise ValueError("Invalid JSON structure: incorrect fields")

    # Check data types.
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

    # Confirm the event can be converted to valid JSON.
    json.loads(json.dumps(event))

    return True


if __name__ == "__main__":
    print("Starting AtmoSync Sensor Simulator...")
    print("Press Ctrl + C to stop.\n")

    try:
        while True:
            sensor_event = generate_sensor_event()

            if validate_event(sensor_event):
                print(json.dumps(sensor_event))

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nSensor simulation stopped.")