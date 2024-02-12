from pydantic import BaseModel, EmailStr


class UserCreateModel(BaseModel):
    """Модель для создания пользователя"""
    username: str
    email: EmailStr
    password: str
    name: str
    surname: str
    father_name: str


class UserOutModel(BaseModel):
    """Модель для вывода информации о пользователе"""
    username: str
    email: EmailStr
    name: str
    surname: str
    father_name: str
