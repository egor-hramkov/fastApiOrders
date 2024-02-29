from pydantic import BaseModel, Field, EmailStr

from apps.notifications.abstract import AbstractNotification
from apps.notifications.enums.notification_events_enum import NotificationEventsEnum
from apps.notifications.enums.notification_types_enum import NotificationTypesEnum


class EmailSchema(BaseModel):
    """Схема email-сообщения"""
    recipients: list[EmailStr] = Field(default_factory=list)
    subject: str
    message: str


class NotificationOrderStatusSchema(AbstractNotification):
    """Уведомление, связанное со статусом заказа"""
    order_id: int
    old_status: str
    new_status: str
    notification_type: str = NotificationTypesEnum.order_status_notification

    def build_notification(self) -> dict:
        return {
            "event": NotificationEventsEnum.changed_order_status.value,
            "id": "message_id",
            "data": f"Статус вашего заказа {self.order_id} изменился с {self.old_status} на {self.new_status}"
        }
