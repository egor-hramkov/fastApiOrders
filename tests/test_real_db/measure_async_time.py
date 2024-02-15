import time
import aiohttp
import asyncio
import concurrent.futures as pool

"""
МОДУЛЬ БЫЛ СДЕЛАН ДЛЯ РАЗОВЫХ ЗАМЕРОВ ВРЕМЕНИ
НЕ ЗАПУСКАТЬ - ЗАСОРЯЕТ БД!
"""


class AsyncRepositoryTest:
    """Тест для замера времени асинхронных запросов"""
    executor = pool.ThreadPoolExecutor(max_workers=40)
    temp_id = 1

    async def get_all_users(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:8000/user/all') as resp:
                ...

    async def create_user(self):
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
        async with aiohttp.ClientSession() as session:
            async with session.post('http://127.0.0.1:8000/user/register', json=register_data) as resp:
                ...

    async def delete_user(self):
        async with aiohttp.ClientSession() as session:
            async with session.delete(f'http://127.0.0.1:8000/user/test_{self.temp_id}') as resp:
                ...

    async def run_test(self):
        tasks = []
        for _ in range(40):
            tasks.append(self.create_user())
            tasks.append(self.get_all_users())
            tasks.append(self.delete_user())
        start = time.time()
        results = await asyncio.gather(*tasks)
        time_result = time.time() - start
        print(f"Асинхронщина отработала за {time_result:.6f} секунд")


if __name__ == '__main__':
    asyncio.run(AsyncRepositoryTest().run_test())
