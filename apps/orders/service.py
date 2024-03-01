import asyncio
from threading import Thread

from apps.notifications.schemas import EmailSchema
from apps.notifications.service import EmailNotificationService
from apps.orders.enums.order_statuses_enum import OrderStatusEnum
from apps.orders.repository import OrderRepository
from apps.orders.schemas import OrderSchema, OrderIn, OrderUpdateSchema
from redis_layer.redis_client import RedisClient


class OrderService:
    """Сервис для работы с заказами"""
    _repository = OrderRepository()

    async def get_order(self, order_id: int) -> OrderSchema:
        """Получение заказа"""
        return await self._repository.get_order(order_id)

    async def create_order(self, order: OrderIn, user_id: int) -> OrderSchema:
        """Создание заказа"""
        return await self._repository.create(order, user_id)

    async def delete_order(self, order_id: int) -> None:
        """Удаление заказа"""
        return await self._repository.delete_order(order_id)

    async def update_order(self, order_id: int, order: OrderUpdateSchema) -> OrderSchema:
        """Удаление заказа"""
        changed_order = await self._repository.update(order_id, order)
        await self.send_notification_status_changed(changed_order)
        return changed_order

    async def update_order_status(self, order_id: int, status: str) -> OrderSchema:
        """Обновление статуса заказа"""
        changed_order = await self._repository.update_order_status(order_id, status)
        await self.send_notification_status_changed(changed_order)
        return changed_order

    @staticmethod
    async def send_notification_status_changed(order: OrderSchema) -> None:
        """Отправляет уведомления по изменению статуса заказа"""
        old_status = order.old_status
        new_status = order.status
        allowed_statuses_for_email = [OrderStatusEnum.done, OrderStatusEnum.canceled]
        if new_status in allowed_statuses_for_email:
            email = EmailSchema.build_email_order_status_changed(order)
            thread = Thread(
                target=asyncio.run, args=(EmailNotificationService.send_notification(email),)
            )
            thread.start()
        if old_status != new_status:
            await RedisClient.create_notification_changed_order_status(order)
