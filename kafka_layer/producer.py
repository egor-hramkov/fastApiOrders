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
        'user_id': 2,
        'order_id': 2,
        'user_email': "test@mail.ru"
    }
    print(f"{producer.bootstrap_connected()=}")
    producer.send(KAFKA_TOPIC, order)
    producer.flush()
    print("Sent order details {} to kafka topic: {}".format(order, KAFKA_TOPIC))


if __name__ == '__main__':
    main()
