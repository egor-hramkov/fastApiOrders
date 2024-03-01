from enum import Enum

from apps.utils.enum_helpers import EnumContainsMixin


class OrderStatusEnum(str, Enum, metaclass=EnumContainsMixin):
    """Енам статусов заказа"""

    created = 'created'
    in_process = 'in_process'
    done = 'done'
    canceled = 'canceled'
