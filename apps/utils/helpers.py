import time
from functools import wraps


def sync_measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        time_result = time.time() - start
        print(f"Функция {func.__name__} отработала за {time_result:.6f} секунд")
        return result

    return wrapper
