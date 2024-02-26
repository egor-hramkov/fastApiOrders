from pydantic import BaseModel

from tests.items.item_utils import TestItem
from tests.users.users_utils import TestUser


class TestOrder(BaseModel):
    """Тестовый класс с данными заказа"""
    id: int = None
    status: str = 'created'
    items: list[TestItem]
    user: TestUser


def get_test_order_create_data():
    """Тестовые данные для создания заказа"""
    return {
        "items": [
            {
                "id": 1
            },
            {
                "id": 2
            }
        ]
    }
