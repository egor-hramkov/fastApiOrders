from typing import Any

from fastapi import APIRouter, HTTPException
from apps.user.schemas import UserCreateModel, UserOutModel, UserUpdateModel
from apps.user.service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"]
)
service = UserService


@router.get('/all', response_model=list[UserOutModel])
async def get_all_users() -> Any:
    all_users = await service().get_all_users()
    return all_users


@router.post('/register', response_model=UserOutModel)
async def register(user_data: UserCreateModel) -> Any:
    user = await service().create_user(user_data)
    return user


@router.get("/{user_id}", response_model=UserOutModel)
async def get_user(user_id: int) -> Any:
    """Получение информации по пользователю"""
    user = await service().get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь с такими данными не найден')
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int) -> None:
    """Удаление пользователя"""
    user = await service().delete_user(user_id)
    return user


@router.put("/{user_id}", response_model=UserOutModel)
async def update_user(user_id: int, user_data: UserUpdateModel) -> Any:
    user = await service().update_user(user_id, user_data)
    return user
