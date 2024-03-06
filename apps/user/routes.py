from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Query
from fastapi_filter import FilterDepends

from apps.user.filters.user_filter import UserFilter
from apps.user.filters.users_filter import AllUserFilter
from apps.user.schemas import UserCreateModel, UserOutModel, UserUpdateModel
from apps.user.service import UserService
from apps.user.utils import USER_RESPONSE

router = APIRouter(
    prefix="/user",
    tags=["user"]
)
service = UserService()


@router.get('/all', response_model=list[UserOutModel])
async def get_all_users(
        all_user_filter=FilterDepends(AllUserFilter),
        skip: int = Query(ge=0, default=0),
        offset: int = Query(ge=0, default=0)
) -> Any:
    all_users = await service.get_all_users(all_user_filter)
    return all_users


@router.post('/register', response_model=UserOutModel)
async def register(user_data: UserCreateModel) -> Any:
    user = await service.create_user(user_data)
    return user


@router.get("/", response_model=UserOutModel)
async def get_user_by_params(user_filter=FilterDepends(UserFilter)) -> Any:
    user = await service.get_user_with_filter(user_filter)
    return user


@router.get("/{user_id}", response_model=UserOutModel)
async def get_user(user_id: int) -> Any:
    """Получение информации по пользователю"""
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь с такими данными не найден')
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int) -> dict[str, str]:
    """Удаление пользователя"""
    await service.delete_user(user_id)
    return USER_RESPONSE['OK_DELETE_RESPONSE']


@router.put("/{user_id}", response_model=UserOutModel)
async def update_user(user_id: int, user_data: UserUpdateModel) -> Any:
    user = await service.update_user(user_id, user_data)
    return user
