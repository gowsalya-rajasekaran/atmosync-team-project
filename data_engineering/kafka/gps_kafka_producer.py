
import json
from kafka import KafkaProducer

from gps_simulator import generate_gps_events

KAFKA_SERVER = "localhost:9092"
GPS_TOPIC = "atmosync-gps-data"


def main():
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_SERVER],
        value_serializer=lambda event: json.dumps(event).encode("utf-8"),
        acks="all"
    )

    print("AtmoSync GPS Kafka Producer Started!")

    try:
        gps_events = generate_gps_events()

        for event in gps_events:
            future = producer.send(GPS_TOPIC, value=event)
            metadata = future.get(timeout=10)

            print(
                f"GPS event sent: {event['event_id']} "
                f"| Topic: {metadata.topic} "
                f"| Partition: {metadata.partition} "
                f"| Offset: {metadata.offset}"
            )

        producer.flush()
        print(f"Successfully sent {len(gps_events)} GPS events!")

    finally:
        producer.close()
        print("GPS Producer closed.")


if __name__ == "__main__":
    main()


import json
from kafka import KafkaProducer

from gps_simulator import generate_gps_events

KAFKA_SERVER = "localhost:9092"
GPS_TOPIC = "atmosync-gps-data"


def main():
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_SERVER],
        value_serializer=lambda event: json.dumps(event).encode("utf-8"),
        acks="all"
    )

    print("AtmoSync GPS Kafka Producer Started!")

    try:
        gps_events = generate_gps_events()

        for event in gps_events:
            future = producer.send(GPS_TOPIC, value=event)
            metadata = future.get(timeout=10)

            print(
                f"GPS event sent: {event['event_id']} "
                f"| Topic: {metadata.topic} "
                f"| Partition: {metadata.partition} "
                f"| Offset: {metadata.offset}"
            )

        producer.flush()
        print(f"Successfully sent {len(gps_events)} GPS events!")

    finally:
        producer.close()
        print("GPS Producer closed.")


if __name__ == "__main__":
    main()
