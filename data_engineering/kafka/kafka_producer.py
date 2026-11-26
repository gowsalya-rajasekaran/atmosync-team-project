from kafka import KafkaProducer
import json
import time

from sensor_simulator import generate_sensor_event, validate_event

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

topic = "atmosync-sensor-data"

print("AtmoSync Kafka Producer Started!")

try:
    for i in range(10):
        sensor_data = generate_sensor_event()

        if validate_event(sensor_data):
            producer.send(topic, value=sensor_data)
            print("Message sent:", sensor_data)

        time.sleep(2)

    producer.flush()
    print("All sensor events sent successfully!")

finally:
    producer.close()
    print("Kafka Producer closed.")
