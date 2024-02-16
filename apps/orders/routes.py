from typing import Annotated

from fastapi import APIRouter, Depends
from apps.auth.oauth2 import OAuth2
from apps.orders.schemas import Order
from apps.orders.service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

service = OrderService()


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str, current_user: Annotated[dict, Depends(OAuth2.get_current_user)]):
    """Получение заказа"""
    ...


@router.post("/create", response_model=Order)
def create_order(order: Order, current_user: Annotated[dict, Depends(OAuth2.get_current_user)]):
    """Создание заказа"""
    service.create_order(order)
