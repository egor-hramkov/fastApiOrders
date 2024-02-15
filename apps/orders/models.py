from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy_utils import ChoiceType

from apps.orders.enums import OrderStatusEnum
from apps.user.models import User
from database.base_models import Base


class Item(Base):
    """Модель товара"""
    __tablename__ = "items"

    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"Item({self.name=}, {self.price=})"


class Order(Base):
    """Модель заказа"""
    __tablename__ = "orders"

    status: Mapped[Enum] = mapped_column(Enum(OrderStatusEnum), default=OrderStatusEnum.created)
    user: Mapped["User"] = relationship("User", foreign_keys=User.id)

    def __repr__(self) -> str:
        return f"Order({self.id=}, {self.user.name=}, {self.user.surname=}, {self.user.father_name=})"
