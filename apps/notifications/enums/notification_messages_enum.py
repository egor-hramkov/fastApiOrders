from enum import Enum


class NotificationMessagesEnum(str, Enum):
    """Распространённые текста уведомлений"""
    order_status_changed = "Статус вашего заказа {order_id} изменился с {old_status} на {new_status}"
