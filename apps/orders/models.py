from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from apps.items.models import Item
from apps.orders.enums.order_statuses_enum import OrderStatusEnum
from apps.user.models import User
from database.base_models import Base


class Order(Base):
    """Модель заказа"""
    __tablename__ = "orders"

    status: Mapped[Enum] = mapped_column(Enum(OrderStatusEnum), default=OrderStatusEnum.created)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship("User")

    def __repr__(self) -> str:
        return f"Order({self.id=}, {self.user.name=}, {self.user.surname=}, {self.user.father_name=})"


class OrderItem(Base):
    """Связь многие-ко-многим заказы с товарами"""
    __tablename__ = "orders_items"

    order: Mapped["Order"] = relationship("Order", cascade="all,delete")
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    item: Mapped["Item"] = relationship("Item", cascade="all,delete")
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"))
