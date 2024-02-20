from typing import TypeVar

from pydantic import BaseModel as PydenticModel
from database.base_models import Base as DatabaseModel

import time
from functools import wraps

D = TypeVar('D', bound=DatabaseModel)


class SchemaMapper:
    """Маппер для динамического преобразования схемы в модель БД"""

    def __init__(self, pydentic_model: PydenticModel, db_model: D):
        self.pydentic_model = pydentic_model
        self.db_model = db_model

    def py_to_db_model(self) -> D:
        """Маппит pydantic model в database model"""
        new_item = self.db_model
        for field in self.pydentic_model.model_fields:
            if field == 'id':
                continue
            new_item.__setattr__(field, getattr(self.pydentic_model, field))
        return new_item


def sync_measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        time_result = time.time() - start
        print(f"Функция {func.__name__} отработала за {time_result:.6f} секунд")
        return result

    return wrapper
