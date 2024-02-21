import json
from kafka import KafkaProducer
from settings.kafka_settings import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    security_protocol="PLAINTEXT",
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)


def main():
    order = {
        'order_id': 10,
        'status': 'in_process'
    }
    producer.send(KAFKA_TOPIC, order)
    producer.flush()


if __name__ == '__main__':
    main()
