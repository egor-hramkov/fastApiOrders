from decimal import Decimal

from pydantic import BaseModel, Field


class ItemSchema(BaseModel):
    """Сущность товара"""
    name: str
    price: Decimal = Field(gt=0)


class ItemInOrder(BaseModel):
    """Товары в запросе заказа"""
    id: int
    name: str
