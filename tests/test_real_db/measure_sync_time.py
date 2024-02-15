import time
from concurrent.futures import as_completed

import requests
import concurrent.futures as pool

"""
МОДУЛЬ ИСПОЛЬЗОВАЛСЯ ДЛЯ ЗАМЕРА ВРЕМЕНИ СИНХРОННОГО ЦИКЛА РАБОТЫ
БОЛЕЕ НЕ ЗАПУСКАТЬ!
"""


class SyncRepositoryTest:
    """Тест для сравнения синхронного и асинхронного репозитория"""
    executor = pool.ThreadPoolExecutor(max_workers=40)
    temp_id = 1

    def sync_get_all_users(self):
        r = requests.get('http://127.0.0.1:8000/user/all')
        return r

    def sync_create_user(self):
        temp_id = self.temp_id
        register_data = {
            "username": f"test_{temp_id}",
            "email": f"test_{temp_id}@example.com",
            "password": "test",
            "name": "test",
            "surname": f"test_{temp_id}",
            "father_name": "string"
        }
        self.temp_id += 1
        r = requests.post('http://127.0.0.1:8000/user/register', json=register_data)
        return r

    def sync_delete_user(self):
        r = requests.delete(f'http://127.0.0.1:8000/user/delete/test_{self.temp_id}')
        self.temp_id += 1
        return r

    def all_sync_cycle(self):
        self.sync_create_user()
        self.sync_get_all_users()
        self.sync_delete_user()

    def run_sync_test(self):
        futures = []
        for _ in range(40):
            futures.append(self.executor.submit(self.all_sync_cycle))
        for future in as_completed(futures):
            result = future.result()


if __name__ == '__main__':
    start = time.time()
    SyncRepositoryTest().run_sync_test()
    time_result = time.time() - start
    print(f"Синхронщина отработала за {time_result:.6f} секунд")
    # 10.1 - 10.6 sec
