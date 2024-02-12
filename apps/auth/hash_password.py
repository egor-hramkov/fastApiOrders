from passlib.context import CryptContext


class HashPassword:
    password_context = CryptContext(schemes='bcrypt', deprecated='auto')

    @classmethod
    def bcrypt(cls, password: str):
        return cls.password_context.hash(password)

    @classmethod
    def verify(cls, hashed_password, plain_password):
        return cls.password_context.verify(plain_password, hashed_password)
