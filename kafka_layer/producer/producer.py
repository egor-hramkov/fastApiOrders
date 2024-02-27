import json

from kafka import KafkaProducer

from settings.kafka_settings import KAFKA_BOOTSTRAP_SERVERS

kafka_producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    security_protocol="PLAINTEXT",
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)
