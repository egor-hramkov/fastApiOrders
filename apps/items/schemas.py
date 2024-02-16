from decimal import Decimal

from pydantic import BaseModel, Field


class ItemSchema(BaseModel):
    """Сущность товара"""
    name: str
    price: Decimal = Field(gt=0)
