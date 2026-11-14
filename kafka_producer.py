from kafka import KafkaProducer
import json
import time

from sensor_simulator import generate_sensor_event

# Connect to Kafka server
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Kafka topic name
topic = 'atmosync-sensor-data'

print("AtmoSync Kafka Producer Started!")

# Generate and publish sensor events
for i in range(10):

    sensor_data = generate_sensor_event()

    producer.send(topic, value=sensor_data)

    print("Message sent:", sensor_data)

    time.sleep(2)

producer.flush()
producer.close()

print("All sensor events sent successfully!")