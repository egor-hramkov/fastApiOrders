from pydantic import BaseModel, Field, ConfigDict

from apps.items.schemas import ItemSchema, ItemInOrder
from apps.orders.models import Order
from apps.user.schemas import UserOutModel


class OrderSchema(BaseModel):
    """Сущность заказа"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int = None
    status: str
    items: list[ItemSchema] = Field(default_factory=list)
    user: UserOutModel

    @staticmethod
    async def build_order_schema(order: Order, user: UserOutModel, items: list[ItemSchema]) -> "OrderSchema":
        """Собирает сущность"""
        return OrderSchema(id=order.id, status=order.status, items=items, user=user)


class OrderIn(BaseModel):
    """Сущность входных параметров заказа"""
    items: list[ItemInOrder] = Field(default_factory=list)


class OrderUpdateSchema(OrderIn):
    """Сущность обновления заказа"""
    status: str
