import aiobcrypt


class HashPassword:
    """Класс для хеширования пароля"""

    @classmethod
    async def bcrypt(cls, password: str):
        salt = await aiobcrypt.gensalt()
        encode_password = str.encode(password)
        hashed_password = await aiobcrypt.hashpw(encode_password, salt)
        return hashed_password.decode()

    @classmethod
    async def verify(cls, hashed_password, plain_password):
        valid_password = await aiobcrypt.checkpw(str.encode(plain_password), str.encode(hashed_password))
        return valid_password
