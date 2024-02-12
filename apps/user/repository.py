from sqlalchemy.exc import IntegrityError

from apps.auth.hash_password import HashPassword
from apps.user import models
from apps.user.exceptions import UserAlreadyExistsException
from apps.user.models import User
from apps.user.schemas import UserCreateModel, UserUpdateModel, BaseUser
from apps.user.utils import ExceptionParser
from database.sql_alchemy import session


class UserRepository:
    """Репозиторий для работы с пользователем"""
    session = session

    def get_all_users(self) -> list[User]:
        with self.session as db:
            return db.query(User).all()

    def get_user(self, user_id: int = None, email: str = None, username: str = None) -> User:
        """Получение пользователя"""
        with self.session as db:
            if user_id:
                return db.query(User).filter(User.id == user_id).first()
            if email:
                return db.query(User).filter(User.email == email).first()
            if username:
                return db.query(User).filter(User.username == username).first()

    def create_user(self, user_data: UserCreateModel) -> User:
        """Создание пользователя"""
        with self.session as db:
            new_user = self.__build_user(user_data)
            try:
                db.add(new_user)
                db.commit()
                db.refresh(new_user)  # get id to new user
            except IntegrityError as e:
                value = ExceptionParser.parse_user_unique_exception(e)
                raise UserAlreadyExistsException(value)
        return new_user

    def update_user(self, user_id: int, user: UserUpdateModel):
        db_user = self.__build_user(user, user_id=user_id)
        with self.session as db:
            try:
                db.add(db_user)
                db.commit()
                db.refresh(db_user)  # get id to new user
            except IntegrityError as e:
                value = ExceptionParser.parse_user_unique_exception(e)
                raise UserAlreadyExistsException(value)
        return db_user

    def delete_user(self, user_id: int) -> User:
        with self.session as db:
            db_user = self.get_user(user_id=user_id)
            db.delete(db_user)
            db.commit()
        return db_user

    def __build_user(self, user_data: UserCreateModel | UserUpdateModel, user_id: int = None) -> User:
        if user_id is None:
            user = models.User()
        else:
            user = self.get_user(user_id=user_id)
        user.username = user_data.username
        user.email = user_data.email
        user.surname = user_data.surname
        user.father_name = user_data.father_name
        user.name = user_data.name
        user.password = HashPassword.bcrypt(user_data.password)
        return user
