from dataclasses import dataclass


def get_test_user_data():
    """Возвращает тестовые данные пользователя для регистрации"""
    return {
        "username": "test123",
        "email": "test123@example.com",
        "name": "string123",
        "surname": "string123",
        "father_name": "string123",
        "password": "string123"
    }


@dataclass
class TestUser:
    """Тестовый класс для пользователя"""
    id: int = None
    username: str = None
    email: str = None
    name: str = None
    surname: str = None
    father_name: str = None
