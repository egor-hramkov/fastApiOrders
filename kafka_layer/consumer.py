import asyncio
import json

from kafka import KafkaConsumer
from kafka.errors import kafka_errors

from apps.orders.service import OrderService
from settings.kafka_settings import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP


async def listen():
    print(f"Consumer is listening topic={KAFKA_TOPIC}, server={KAFKA_BOOTSTRAP_SERVERS}, group={KAFKA_CONSUMER_GROUP}")
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
        group_id=KAFKA_CONSUMER_GROUP,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    for msg in consumer:
        order_data = msg.value
        try:
            await OrderService().update_order_status(order_data['order_id'], order_data['status'])
        except:
            print(f"Что-то пошло не так при изменении статуса заказа")
        else:
            print(f"Статус заказа {order_data['order_id']} изменён на {order_data['status']}")
        try:
            consumer.commit()
        except kafka_errors.CommitFailedError:
            print("Зашли в эксепт")
            continue


def run_consumer():
    asyncio.run(listen())
