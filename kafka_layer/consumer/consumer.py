import json

from kafka import KafkaConsumer

from settings.kafka_settings import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP

kafka_consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    group_id=KAFKA_CONSUMER_GROUP,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
