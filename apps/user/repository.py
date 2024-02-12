from sqlalchemy.exc import IntegrityError

from apps.auth.hash_password import HashPassword
from apps.user import models
from apps.user.exceptions import UserAlreadyExistsException
from apps.user.models import User
from apps.user.schemas import UserCreateModel
from apps.user.utils import ExceptionParser
from database.sql_alchemy import session


class UserRepository:
    """Репозиторий для работы с пользователем"""
    session = session

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

    @staticmethod
    def __build_user(user_data: UserCreateModel) -> User:
        new_user = models.User()
        new_user.username = user_data.username
        new_user.email = user_data.email
        new_user.surname = user_data.surname
        new_user.father_name = user_data.father_name
        new_user.name = user_data.name
        new_user.password = HashPassword.bcrypt(user_data.password)
        return new_user
