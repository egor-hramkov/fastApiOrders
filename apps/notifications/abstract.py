from abc import ABC

from pydantic import BaseModel


class AbstractNotification(BaseModel, ABC):
    """Абстрактный класс уведомления"""
    notification_type: str

    @staticmethod
    def build_notification() -> dict:
        raise NotImplementedError
