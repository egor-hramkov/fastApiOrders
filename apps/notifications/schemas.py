from pydantic import BaseModel, Field, EmailStr

from apps.notifications.abstract import AbstractNotification
from apps.notifications.enums.notification_events_enum import NotificationEventsEnum
from apps.notifications.enums.notification_messages_enum import NotificationMessagesEnum
from apps.notifications.enums.notification_subjects_enum import NotificationSubjectsEnum
from apps.notifications.enums.notification_types_enum import NotificationTypesEnum
from apps.orders.schemas import OrderSchema


class EmailSchema(BaseModel):
    """Схема email-сообщения"""
    recipients: list[EmailStr] = Field(default_factory=list)
    subject: str
    message: str

    @staticmethod
    def build_email_order_status_changed(order: OrderSchema):
        """Собирает емаил сообщение об изменении статуса заказа"""
        return EmailSchema(
            recipients=[order.user.email],
            subject=NotificationSubjectsEnum.order_status_changed.value,
            message=NotificationMessagesEnum.order_status_changed.value.format(
                order_id=order.id, old_status=order.old_status.value, new_status=order.status.value
            )
        )


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
