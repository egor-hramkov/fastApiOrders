from enum import Enum


class NotificationEventsEnum(str, Enum):
    """Enum for notification events"""

    changed_order_status = "Изменение статуса заказа"
