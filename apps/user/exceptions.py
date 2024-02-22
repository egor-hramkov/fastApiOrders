from fastapi import HTTPException
from starlette import status


class UserAlreadyExistsException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = '',
    headers = {'WWW-Authneticate': 'Bearer'}

    def __init__(self, value: str):
        self.detail = f"Пользователь с таким {value} уже существует"
        super().__init__(self.status_code, self.detail, self.headers)


class UserDoesNotExistsException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Пользователь не найден в системе',
    headers = {'WWW-Authneticate': 'Bearer'}

    def __init__(self):
        super().__init__(self.status_code, self.detail, self.headers)
