from apps.orders.repository import OrderRepository
from apps.orders.schemas import OrderSchema, OrderIn


class OrderService:
    """Сервис для работы с заказами"""
    _repository = OrderRepository()

    async def get_order(self, order_id: int, user_id: int) -> OrderSchema:
        """Получение заказа"""
        return await self._repository.get(order_id, user_id)

    async def create_order(self, order: OrderIn, user_id: int) -> OrderSchema:
        """Создание заказа"""
        return await self._repository.create(order, user_id)

    async def delete_order(self, order_id: int) -> None:
        """Удаление заказа"""
        return await self._repository.delete(order_id)
