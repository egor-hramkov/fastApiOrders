from pydantic import BaseModel, Field, EmailStr


class EmailSchema(BaseModel):
    """Схема email-сообщения"""
    recipients: list[EmailStr] = Field(default_factory=list)
    subject: str
    message: str
