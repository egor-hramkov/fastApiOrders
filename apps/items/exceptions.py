from fastapi import HTTPException
from starlette import status


class BaseItemException(HTTPException):
    """Базовый класс ошибки для Item"""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = '',
    headers = {'WWW-Authneticate': 'Bearer'}


class ItemAlreadyExistsException(BaseItemException):
    """Ошибка - такой товар уже существует"""

    def __init__(self, value: str):
        self.detail = f"Товар {value} уже существует"
        super().__init__(self.status_code, self.detail, self.headers)


class ItemDoesNotExistException(BaseItemException):
    """Ошибка - товар не найден"""

    def __init__(self):
        self.detail = f"Товар не найден"
        super().__init__(self.status_code, self.detail, self.headers)


class ItemsDoesNotExistException(BaseItemException):
    """Ошибка - множество товаров не найдено"""

    def __init__(self, value: set | list):
        self.detail = f"Товары с id: {value} не существуют"
        super().__init__(self.status_code, self.detail, self.headers)
