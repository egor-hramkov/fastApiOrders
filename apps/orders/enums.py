from enum import Enum

from apps.utils.enum_helpers import EnumContainsMixin


class OrderStatusEnum(str, Enum, metaclass=EnumContainsMixin):
    """Енам статусов заказа"""

    created = 'Заказ создан'
    in_process = 'Заказ в процессе'
    done = 'Заказ готов'
    canceled = 'Заказ отменён'


