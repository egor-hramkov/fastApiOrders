from apps.notifications.abstract import AbstractNotification
from apps.notifications.enums.notification_types_enum import NotificationTypesEnum
from apps.notifications.exception import WrongNotificationTypeException
from apps.notifications.schemas import NotificationOrderStatusSchema


class NotificationFactory:
    """Фабрика классов уведомлений"""
    classes = {
        NotificationTypesEnum.order_status_notification: NotificationOrderStatusSchema
    }

    @classmethod
    async def get_notification_class(cls, data: dict) -> AbstractNotification:
        for notification_type in NotificationTypesEnum:
            if data.get(notification_type):
                fabric_class = cls.classes[notification_type]
                return fabric_class(**data[notification_type])
        raise WrongNotificationTypeException()
