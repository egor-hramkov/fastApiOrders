from dataclasses import dataclass
from decimal import Decimal

from pydantic import BaseModel, Field


#@dataclass
class TestItem(BaseModel):
    """Тестовый класс для товара"""
    id: int = None
    name: str = None
    price: Decimal = Field(gt=0, default=10)


def get_test_item_data():
    """Возвращает тестовые данные пользователя для регистрации"""
    return {
        "name": "test item",
        "price": 100
    }
