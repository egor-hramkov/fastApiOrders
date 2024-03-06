import asyncio
import logging
import traceback

from kafka.errors import kafka_errors

from apps.orders.service import OrderService
from kafka_layer.consumer.consumer import kafka_consumer
from settings.kafka_settings import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP

logger = logging.getLogger(__name__)


async def listen():
    logger.info(
        f"Consumer is listening topic={KAFKA_TOPIC}, server={KAFKA_BOOTSTRAP_SERVERS}, group={KAFKA_CONSUMER_GROUP}"
    )
    consumer = kafka_consumer
    order_service = OrderService()
    for msg in consumer:
        order_data = msg.value
        try:
            await order_service.update_order_status(order_data['order_id'], order_data['status'])
        except Exception as e:
            logger.error(
                f"Что-то пошло не так при изменении статуса заказа: " + str(e) + traceback.format_exc()
            )
        else:
            logger.info(f"Статус заказа {order_data['order_id']} изменён на {order_data['status']}")

        try:
            consumer.commit()
        except kafka_errors.CommitFailedError:
            continue


def run_consumer():
    asyncio.run(listen())
