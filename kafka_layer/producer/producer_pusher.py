from kafka_layer.producer.producer import kafka_producer
from settings.kafka_settings import KAFKA_TOPIC

producer = kafka_producer


def main():
    order = {
        'order_id': 2,
        'status': 'created'
    }
    producer.send(KAFKA_TOPIC, order)
    producer.flush()


if __name__ == '__main__':
    main()
