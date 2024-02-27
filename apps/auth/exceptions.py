from fastapi import HTTPException
from starlette import status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Не удалось подтвердить учетные данные',
    headers={'WWW-Authneticate': 'Bearer'}
)


class TokenExpireException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Истёк срок действия токена'
    headers = {'WWW-Authneticate': 'Bearer'}

    def __init__(self):
        super().__init__(self.status_code, self.detail, self.headers)

