from kafka import KafkaConsumer
from kafka.errors import kafka_errors

from settings.kafka_settings import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP


def run_consumer():
    print(f"Consumer is listening topic={KAFKA_TOPIC}, server={KAFKA_BOOTSTRAP_SERVERS}, group={KAFKA_CONSUMER_GROUP}")
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
        group_id=KAFKA_CONSUMER_GROUP,
        # value_deserializer=json.load
    )
    for msg in consumer:
        print(msg)
        try:
            # handle_pool_cache_excess()
            consumer.commit()
        except kafka_errors.CommitFailedError:
            # Отлавливаем редкий, но возможный случай исключения
            # при ребалансе
            print("Зашли в эксепт")
            continue
