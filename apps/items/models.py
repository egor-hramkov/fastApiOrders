from _decimal import Decimal
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.base_models import Base


class Item(Base):
    """Модель товара"""
    __tablename__ = "items"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    price: Mapped[Decimal] = mapped_column()

    def __repr__(self) -> str:
        return f"Item({self.name=}, {self.price=})"
