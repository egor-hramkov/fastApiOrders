from enum import Enum

from apps.utils.enum_helpers import EnumContainsMixin


class NotificationTypesEnum(str, Enum, metaclass=EnumContainsMixin):
    """Enum типов уведомлений"""
    order_status_notification = "order_status_notification"
