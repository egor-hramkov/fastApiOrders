from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from apps.user.models import User


class UserFilter(Filter):
    """Фильтр по пользователям"""
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None

    class Constants(Filter.Constants):
        model = User
