from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from apps.user.models import User


class AllUserFilter(Filter):
    """Фильтр по пользователям"""
    username__in: Optional[list[str]] = Field(default=None)
    email__in: Optional[list[str]] = Field(default=None)

    class Constants(Filter.Constants):
        model = User
