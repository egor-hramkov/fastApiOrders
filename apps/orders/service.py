from apps.orders.repository import OrderRepository


class OrderService:
    """Сервис для работы с заказами"""
    _repository = OrderRepository()

    def get_order(self, order_id: int) -> dict:
        """Получение заказа"""
        ...

    def create_order(self, order: dict) -> dict:
        """Создание заказа"""
        ...
