from fastapi import HTTPException
from starlette import status


class OrderAlreadyExistsException(HTTPException):
    """Ошибка - заказ уже существует"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = '',
    headers = {'WWW-Authneticate': 'Bearer'}

    def __init__(self, value: str):
        self.detail = f"Заказ {value} уже существует"
        super().__init__(self.status_code, self.detail, self.headers)


class OrderDoesNotExistsException(HTTPException):
    """Заказ не существует"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Данного заказа не существует',
    headers = {'WWW-Authneticate': 'Bearer'}

    def __init__(self):
        super().__init__(self.status_code, self.detail, self.headers)
