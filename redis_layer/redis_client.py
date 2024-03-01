import json

from redis.asyncio import Redis, from_url

from apps.notifications.enums.notification_types_enum import NotificationTypesEnum
from apps.orders.schemas import OrderSchema
from settings.redis_settings import REDIS_SETTINGS


class RedisClient:
    """Класс для логики клиента редис"""
    redis_client: Redis = None

    @classmethod
    async def init_redis_pool(cls):
        cls.redis_client = from_url(
            REDIS_SETTINGS['URL'],
            encoding="utf-8",
            decode_responses=True
        )

    @classmethod
    async def update_value(cls, redis_key: str | int, new_data: dict):
        # ToDo костыль открывать новое соединение каждый раз. Т.К. из двух разных потоков появляется эксепшн
        await cls.init_redis_pool()
        raw_redis_data = await cls.redis_client.get(str(redis_key))
        if raw_redis_data is None:
            data = {}
        else:
            data: dict = json.loads(raw_redis_data)
        data.update(new_data)
        await cls.redis_client.set(str(redis_key), json.dumps(data))

    @classmethod
    async def create_notification_changed_order_status(cls, order: OrderSchema):
        """Создаёт уведомление в Redis об изменении статуса заказа"""
        data = {
            NotificationTypesEnum.order_status_notification: {
                "order_id": order.id,
                "new_status": order.status,
                "old_status": order.old_status
            }
        }
        await cls.update_value(order.user.id, data)

    @classmethod
    async def delete_redis_key(cls, redis_key: str):
        # ToDo костыль открывать новое соединение каждый раз. Т.К. из двух разных потоков появляется эксепшн
        await cls.init_redis_pool()
        await cls.redis_client.delete(redis_key)

    @classmethod
    async def get_notifications(cls, user_id: int) -> dict | None:
        """Получение уведомлений пользователя"""
        # ToDo костыль открывать новое соединение каждый раз. Т.К. из двух разных потоков появляется эксепшн
        await cls.init_redis_pool()
        raw_redis_data = await cls.redis_client.get(str(user_id))
        if raw_redis_data is None:
            return
        return json.loads(raw_redis_data)

    @classmethod
    async def delete_sent_notifications(cls, redis_key: str, data_key: str) -> None:
        """Удаляет из redis ячейки redis_key уведомление с ключом data_key"""
        # ToDo костыль открывать новое соединение каждый раз. Т.К. из двух разных потоков появляется эксепшн
        await cls.init_redis_pool()
        raw_redis_data = await cls.redis_client.get(redis_key)
        notification_data: dict = json.loads(raw_redis_data)
        notification_data.pop(data_key)
        await cls.redis_client.set(redis_key, json.dumps(notification_data))
