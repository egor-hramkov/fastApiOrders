from typing import Any

from fastapi import APIRouter, Depends
from apps.auth.oauth2 import OAuth2
from apps.orders.schemas import OrderSchema, OrderIn, OrderUpdateSchema
from apps.orders.service import OrderService
from apps.user.schemas import UserOutModel

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

service = OrderService()


@router.get("/{order_id}", response_model=OrderSchema)
async def get_order(order_id: int, current_user: UserOutModel = Depends(OAuth2().get_current_user)) -> Any:
    """Получение заказа"""
    order = await service.get_order(order_id)
    return order


@router.post("/create", response_model=OrderSchema)
async def create_order(order: OrderIn, current_user: UserOutModel = Depends(OAuth2().get_current_user)) -> Any:
    """Создание заказа"""
    order = await service.create_order(order, current_user.id)
    return order


@router.delete("/{order_id}")
async def delete_order(order_id: int, current_user: UserOutModel = Depends(OAuth2().get_current_user)) -> dict[str, str]:
    """Обновление заказа"""
    await service.delete_order(order_id)
    return {"result": "Заказ успешно удалён"}


@router.put("/{order_id}", response_model=OrderSchema, tags=["orders"])
async def update_order(
        order_id: int,
        order: OrderUpdateSchema,
        current_user: UserOutModel = Depends(OAuth2().get_current_user)
) -> Any:
    """Обновление заказа"""
    order = await service.update_order(order_id, order)
    return order
