from sqlalchemy.exc import IntegrityError

from apps.auth.hash_password import HashPassword
from apps.user.exceptions import UserAlreadyExistsException, UserDoesNotExistsException
from apps.user.filters.user_filter import UserFilter
from apps.user.filters.users_filter import AllUserFilter
from apps.user.models import User
from apps.user.schemas import UserCreateModel, UserUpdateModel, UserOutModel
from apps.utils.exception_parser import ExceptionParser
from apps.utils.helpers import SchemaMapper
from database.sql_alchemy import async_session

from sqlalchemy import select, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    """Репозиторий для работы с пользователем"""
    session: AsyncSession = async_session

    async def get_all_users(self, all_user_filter: AllUserFilter) -> list[User]:
        """Получение всех пользователей"""
        async with self.session() as db:
            statement = select(User)
            statement = all_user_filter.filter(statement)
            result = await db.execute(statement)
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
        if user is None:
            raise UserDoesNotExistsException()
        return user

    async def get_user(self, user_id: int = None, email: str = None, username: str = None) -> UserOutModel:
        """Получение пользователя"""
        user = await self.get_raw_user(user_id, email, username)
        return UserOutModel.model_validate(user, from_attributes=True)

    async def get_user_with_filter(self, user_filter: UserFilter) -> UserOutModel:
        """Получение пользователя по фильтрам"""
        async with self.session() as db:
            statement = select(User)
            statement = user_filter.filter(statement)
            result = await db.execute(statement)
            user = result.scalars().first()
            if user is None:
                raise UserDoesNotExistsException()
            return UserOutModel.model_validate(user, from_attributes=True)

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
                value = ExceptionParser.parse_unique_exception(e, ['username', 'email', 'id'])
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
