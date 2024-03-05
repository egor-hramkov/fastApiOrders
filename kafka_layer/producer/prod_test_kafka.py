import json

from kafka import KafkaProducer
# Нужен для ручного запуска в докере, НЕ ОБРАЩАТЬ ВНИМАНИЯ.
kafka_producer = KafkaProducer(
    bootstrap_servers=["localhost:9094"],
    security_protocol="PLAINTEXT",
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)


def main():
    order = {
        'order_id': 2,
        'status': 'created'
    }
    kafka_producer.send("my_topic", order)
    kafka_producer.flush()


if __name__ == '__main__':
    main()
