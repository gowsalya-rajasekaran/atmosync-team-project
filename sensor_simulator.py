import json
import random
import time
from datetime import datetime, timezone

def generate_sensor_event():

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "container_id": random.choice(["CONT001", "CONT002", "CONT003"]),
        "temperature": round(random.uniform(2, 15), 2),
        "humidity": round(random.uniform(40, 90), 2),
        "vibration": round(random.uniform(0.1, 1.0), 2),
        "commodity": random.choice(["Apples", "Bananas", "Mangoes"]),
        "quantity_kg": round(random.uniform(100, 1000), 2)
    }

    return event


if __name__ == "__main__":

    print("Starting AtmoSync Sensor Simulator...\n")

    for i in range(10):

        sensor_data = generate_sensor_event()

        json_event = json.dumps(sensor_data)

        print(json_event)

        time.sleep(2)

    print("\nSimulation completed!")