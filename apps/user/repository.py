from pydantic import parse_obj_as
from sqlalchemy.exc import IntegrityError

from apps.auth.hash_password import HashPassword
from apps.user import models
from apps.user.exceptions import UserAlreadyExistsException
from apps.user.models import User
from apps.user.schemas import UserCreateModel, UserUpdateModel, UserOutModel, UserWithPW
from apps.user.utils import ExceptionParser
from apps.utils.helpers import SchemaMapper
from database.sql_alchemy import async_session

from sqlalchemy import select, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    """Репозиторий для работы с пользователем"""
    session: AsyncSession = async_session

    async def get_all_users(self) -> list[User]:
        """Получение всех пользователей"""
        async with self.session() as db:
            result = await db.execute(select(User))
            return result.scalars()

    async def get_raw_user(self, user_id: int = None, email: str = None, username: str = None) -> User:
        """Получение записи пользователя в БД"""
        async with self.session() as db:
            if user_id:
                result = await db.execute(select(User).filter(User.id == user_id))
            elif email:
                result = await db.execute(select(User).filter(User.email == email))
            elif username:
                result = await db.execute(select(User).filter(User.username == username))
        user = result.scalars().first()
        return user

    async def get_user(self, user_id: int = None, email: str = None, username: str = None) -> UserWithPW:
        """Получение пользователя"""
        user = await self.get_raw_user(user_id, email, username)
        return UserWithPW.model_validate(user, from_attributes=True)

    async def create(self, user_data: UserCreateModel) -> User:
        """Создание пользователя"""
        new_user = await self.__build_user(user_data)
        await self.__save_user(new_user)
        return new_user

    async def update_user(self, user_id: int, user: UserUpdateModel) -> User:
        """Обновляет пользователя"""
        updated_user = await self.__build_user(user, user_id=user_id)
        await self.__save_user(updated_user)
        return updated_user

    async def delete_user(self, user_id: int = None, username: str = None) -> None:
        """Удаляет пользователя"""
        async with self.session() as db:
            stmt = delete(User).where(
                or_(User.id == user_id, User.username == username)
            )
            await db.execute(stmt)
            await db.commit()

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
        if user_id is not None:
            user = await self.get_raw_user(user_id=user_id)
        else:
            user = User()
        mapper = SchemaMapper(user_data, user)
        user = mapper.py_to_db_model()
        user.password = await HashPassword.bcrypt(user_data.password)
        return user
