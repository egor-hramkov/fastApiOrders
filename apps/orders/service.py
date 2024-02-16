from apps.orders.repository import OrderRepository
from apps.orders.schemas import Order


class OrderService:
    """Сервис для работы с заказами"""
    _repository = OrderRepository()

    def get_order(self, order_id: int) -> dict:
        """Получение заказа"""
        ...

    def create_order(self, order: Order) -> dict:
        """Создание заказа"""
        ...
