from enum import Enum


class OrderStatusEnum(str, Enum):
    """Енам статусов заказа"""

    created = 'Заказ создан'
    in_process = 'Заказ в процессе'
    done = 'Заказ готов'
    canceled = 'Заказ отменён'
