from pydantic import BaseModel, EmailStr


class UserOutModel(BaseModel):
    """Модель для вывода информации о пользователе"""
    id: int = None
    username: str
    email: EmailStr
    name: str
    surname: str
    father_name: str


class UserWithPW(UserOutModel):
    """Базовые поля пользователя"""
    password: str


class UserCreateModel(UserWithPW):
    """Модель для создания пользователя"""
    ...


class UserUpdateModel(UserWithPW):
    """Модель для обновления пользователя"""
    ...
