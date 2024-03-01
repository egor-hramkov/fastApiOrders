from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from apps.items.schemas import ItemSchema, ItemInOrder
from apps.orders.enums.order_statuses_enum import OrderStatusEnum
from apps.orders.models import Order
from apps.user.schemas import UserOutModel


class OrderSchema(BaseModel):
    """Сущность заказа"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int = None
    old_status: Optional[OrderStatusEnum] = Field(
        description="Старый статус заказа",
        enum=list(OrderStatusEnum),
        examples=['created'],
        default=None,
    )
    status: OrderStatusEnum = Field(description="Статус заказа", enum=list(OrderStatusEnum), examples=['created'])
    items: list[ItemSchema] = Field(default_factory=list)
    user: UserOutModel

    @staticmethod
    async def build_order_schema(
            order: Order,
            user: UserOutModel,
            items: list[ItemSchema],
            old_status: OrderStatusEnum = None
    ) -> "OrderSchema":
        """Собирает сущность"""
        return OrderSchema(id=order.id, old_status=old_status, status=order.status, items=items, user=user)


class OrderIn(BaseModel):
    """Сущность входных параметров заказа"""
    items: list[ItemInOrder] = Field(default_factory=list)


class OrderUpdateSchema(OrderIn):
    """Сущность обновления заказа"""
    status: OrderStatusEnum = Field(description="Статус заказа", enum=list(OrderStatusEnum))
