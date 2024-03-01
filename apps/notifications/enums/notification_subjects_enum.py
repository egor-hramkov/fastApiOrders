from enum import Enum


class NotificationSubjectsEnum(str, Enum):
    """Enum тем уведомлений"""
    order_status_changed = 'Изменён статус вашего заказа'
