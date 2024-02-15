from pydantic import BaseModel


class Order(BaseModel):
    """Сущность заказа"""
    ...


class OrderCreate(Order):
    """Сущность для создания заказа"""
    ...


class OrderOut(Order):
    """Сущность для ответа с информацией о заказе"""
    ...
