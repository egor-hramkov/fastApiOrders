from fastapi import HTTPException
from starlette import status


class WrongNotificationTypeException(HTTPException):
    """Ошибка при неправильном типе уведомлении"""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Неправильный тип уведомления',
    headers = {'WWW-Authneticate': 'Bearer'}

    def __init__(self):
        super().__init__(self.status_code, self.detail, self.headers)
