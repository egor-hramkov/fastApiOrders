from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import DecodeError

from datetime import datetime, timedelta

from apps.auth.exceptions import credentials_exception, TokenExpireException
from apps.user.repository import UserRepository
from apps.user.schemas import UserOutModel
from settings.auth_settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/token')


class OAuth2:
    _user_repository = UserRepository()
    datetime_format = "%m/%d/%Y, %H:%M:%S"

    async def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        expire_str = expire.strftime(self.datetime_format)
        to_encode.update({'expire': expire_str})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: str = Depends(oauth2_schema)) -> UserOutModel:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            decode_username: str = payload.get('username')

            if decode_username is None:
                raise credentials_exception
        except DecodeError as e:
            raise credentials_exception

        datetime_expire_str = payload['expire']
        datetime_expire = datetime.strptime(datetime_expire_str, self.datetime_format)
        if datetime_expire < datetime.now():
            raise TokenExpireException()

        user = await self._user_repository.get_user(username=decode_username)

        if user is None:
            raise credentials_exception

        return user
