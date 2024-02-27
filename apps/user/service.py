from apps.user.models import User
from apps.user.repository import UserRepository
from apps.user.schemas import UserCreateModel, UserUpdateModel, UserOutModel


class UserService:
    """Сервис для работы с пользователем"""
    # по моему мнению, лучше переопределить метод __init__:
    """
        def __init__(self):
            self.repository = UserRepository()
    """
    # так мы не будем порождать новые экземпляры класса UserRepository, а будем использовать уже существующий
    repository = UserRepository

    async def get_all_users(self) -> list[User]:
        all_users = await self.repository().get_all_users()
        return all_users

    async def get_user(self, user_id: int = None, email: str = None, username: str = None) -> UserOutModel:
        user = await self.repository().get_user(user_id, email, username)
        return user

    async def create_user(self, user_data: UserCreateModel) -> User:
        user = await self.repository().create(user_data)
        return user

    async def update_user(self, user_id: int, user_data: UserUpdateModel) -> User:
        user = await self.repository().update_user(user_id, user_data)
        return user

    async def delete_user(self, user_id: int = None, username: str = None) -> None:
        return await self.repository().delete_user(user_id, username)
