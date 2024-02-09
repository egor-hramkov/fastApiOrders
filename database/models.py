from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)


class User(Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(String(20))
    surname: Mapped[str] = mapped_column(String(25))
    father_name: Mapped[str] = mapped_column(String(25))

    def __repr__(self) -> str:
        return f"User({self.id=}, {self.name=}, {self.surname=}, {self.father_name=})"
