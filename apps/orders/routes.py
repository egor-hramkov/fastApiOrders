from typing import Annotated

from fastapi import APIRouter, Depends
from apps.auth.oauth2 import OAuth2
from apps.orders.schemas import OrderSchema, OrderIn
from apps.orders.service import OrderService
from apps.user.models import User
from apps.user.schemas import BaseUser

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

service = OrderService()


@router.get("/{order_id}", response_model=OrderSchema)
async def get_order(order_id: int, current_user: User = Depends(OAuth2().get_current_user)):
    """Получение заказа"""
    order = await service.get_order(order_id, current_user.id)
    return order


@router.post("/create")
async def create_order(order: OrderIn, current_user: User = Depends(OAuth2().get_current_user)):
    """Создание заказа"""
    order = await service.create_order(order, current_user.id)
    return order
