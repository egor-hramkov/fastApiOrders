from apps.user.models import User
from apps.user.repository import UserRepository
from apps.user.schemas import UserCreateModel, UserUpdateModel


class UserService:
    """Сервис для работы с пользователем"""
    repository = UserRepository

    async def get_user(self, user_id: int = None, email: str = None, username: str = None) -> User:
        return self.repository().get_user(user_id, email, username)

    async def create_user(self, user_data: UserCreateModel) -> User:
        return self.repository().create_user(user_data)

    async def update_user(self, user_id: int, user_data: UserUpdateModel) -> User:
        return self.repository().update_user(user_id, user_data)

    async def delete_user(self, user_id: int) -> User:
        return self.repository().delete_user(user_id)
