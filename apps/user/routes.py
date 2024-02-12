from typing import Any

from fastapi import APIRouter, HTTPException

from apps.user.schemas import UserCreateModel, UserOutModel
from apps.user.service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"]
)
service = UserService


@router.post('/register', response_model=UserOutModel)
async def register(user_data: UserCreateModel) -> Any:
    user = await service().create_user(user_data)
    return user


@router.get("/{user_id}")
async def get_user(user_id: int = None, email: str = None, username: str = None):
    """Получение информации по пользователю"""
    user = await service().get_user(user_id, email, username)
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь с такими данными не найден')
    return user
