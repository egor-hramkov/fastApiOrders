from pydantic import BaseModel, Field

from apps.items.schemas import ItemSchema
from apps.user.schemas import UserOutModel


class Order(BaseModel):
    """Сущность заказа"""
    id: int = None
    items: list[ItemSchema] = Field(default_factory=list)
    user: UserOutModel


class OrderCreate(Order):
    """Сущность для создания заказа"""
    ...


class OrderOut(Order):
    """Сущность для ответа с информацией о заказе"""
    ...
