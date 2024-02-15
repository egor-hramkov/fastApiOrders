from sqlalchemy.exc import IntegrityError

from apps.auth.hash_password import HashPassword
from apps.user import models
from apps.user.exceptions import UserAlreadyExistsException
from apps.user.models import User
from apps.user.schemas import UserCreateModel, UserUpdateModel
from apps.user.utils import ExceptionParser
from database.sql_alchemy import async_session

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    """Репозиторий для работы с пользователем"""
    session: AsyncSession = async_session

    async def get_all_users(self) -> list[User]:
        """Получение всех пользователей"""
        async with self.session() as db:
            result = await db.execute(select(User))
            return result.scalars()

    async def get_user(self, user_id: int = None, email: str = None, username: str = None) -> User | None:
        """Получение пользователя"""
        async with self.session() as db:
            if user_id:
                result = await db.execute(select(User).filter(User.id == user_id))
                return result.scalars().first()
            if email:
                result = await db.execute(select(User).filter(User.email == email))
                return result.scalars().first()
            if username:
                result = await db.execute(select(User).filter(User.username == username))
                return result.scalars().first()

    async def create_user(self, user_data: UserCreateModel) -> User:
        """Создание пользователя"""
        new_user = await self.__build_user(user_data)
        await self.__save_user(new_user)
        return new_user

    async def update_user(self, user_id: int, user: UserUpdateModel) -> User:
        """Обновляет пользователя"""
        updated_user = self.__build_user(user, user_id=user_id)
        await self.__save_user(updated_user)
        return updated_user

    async def delete_user(self, user_id: int = None, username: str = None) -> User:
        """Удаляет пользователя"""
        async with self.session() as db:
            db_user = await self.get_user(user_id=user_id, username=username)
            await db.delete(db_user)
            await db.commit()
        return db_user

    async def __save_user(self, user: User):
        """Сохраняет пользователя в БД"""
        async with self.session() as db:
            try:
                db.add(user)
                await db.commit()
                await db.refresh(user)
            except IntegrityError as e:
                value = ExceptionParser.parse_user_unique_exception(e)
                raise UserAlreadyExistsException(value)

    async def __build_user(self, user_data: UserCreateModel | UserUpdateModel, user_id: int = None) -> User:
        """Собирает сущность пользователя"""
        if user_id is None:
            user = models.User()
        else:
            user = await self.get_user(user_id=user_id)
        user.username = user_data.username
        user.email = user_data.email
        user.surname = user_data.surname
        user.father_name = user_data.father_name
        user.name = user_data.name
        user.password = await HashPassword.bcrypt(user_data.password)
        return user
