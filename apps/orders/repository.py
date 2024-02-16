from sqlalchemy.ext.asyncio import AsyncSession

from database.sql_alchemy import async_session


class OrderRepository:
    """Репозиторий для работы с заказами"""

    session: AsyncSession = async_session

    def get_order(self, order_id: int) -> dict:
        """Получение заказа"""
        ...

    def create(self, order: dict) -> dict:
        """Создание заказа"""
        ...
