from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    """Базовые поля пользователя"""
    username: str
    email: EmailStr
    password: str
    name: str
    surname: str
    father_name: str


class UserCreateModel(BaseUser):
    """Модель для создания пользователя"""
    ...


class UserUpdateModel(BaseUser):
    """Модель для обновления пользователя"""
    ...


class UserOutModel(BaseModel):
    """Модель для вывода информации о пользователе"""
    id: int = None
    username: str
    email: EmailStr
    name: str
    surname: str
    father_name: str
