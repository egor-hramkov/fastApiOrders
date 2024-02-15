from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import DecodeError

from datetime import datetime, timedelta

from apps.auth.exceptions import credentials_exception
from apps.user.repository import UserRepository
from settings.auth_settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


class OAuth2:
    _user_repository = UserRepository()

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def get_current_user(self, token: str = Depends(oauth2_schema)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            decode_username: str = payload.get('username')

            if decode_username is None:
                raise credentials_exception
        except DecodeError:
            raise credentials_exception

        # TODO: check if token expires

        user = self._user_repository.get_user(username=decode_username)

        if user is None:
            raise credentials_exception

        return user
