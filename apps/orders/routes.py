from fastapi import APIRouter, Depends
from apps.auth.oauth2 import OAuth2
from apps.orders.service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

service = OrderService()


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str):
    """Получение заказа"""
    ...


@router.post("/create")
def create_order(order, current_user: Depends(OAuth2.get_current_user)):
    """Создание заказа"""
    ...
