from enum import Enum


class NotificationTypesEnum(str, Enum):
    """Enum типов уведомлений"""
    order_status_notification = "order_status_notification"
