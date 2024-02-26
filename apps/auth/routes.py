from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from apps.auth.oauth2 import OAuth2
from apps.auth.hash_password import HashPassword
from apps.user.repository import UserRepository

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
user_repository = UserRepository()


@router.post('/token')
async def get_token(request: OAuth2PasswordRequestForm = Depends()):
    user = await user_repository.get_raw_user(username=request.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    if not await HashPassword.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wrong password')

    access_token = await OAuth2.create_access_token(data={'username': user.username})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }
