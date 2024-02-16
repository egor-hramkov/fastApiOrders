from fastapi import HTTPException
from starlette import status


class ItemAlreadyExistsException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = '',
    headers = {'WWW-Authneticate': 'Bearer'}

    def __init__(self, value: str):
        self.detail = f"Товар {value} уже существует"
        super().__init__(self.status_code, self.detail, self.headers)
