import requests

from tests.utils import base_app_url


class UsersUtils:
    """Утилиты для тестов API пользователей"""

    base_user_url = f"{base_app_url}/user"

    def get_all_users(self, user_data: dict) -> dict:
        """Регистрация пользователя"""
        register_url = f"{self.base_user_url}/all"
        r = requests.get(register_url)
        return r.json()

    def register_user(self, user_data: dict) -> dict:
        """Регистрация пользователя"""
        register_url = f"{self.base_user_url}/register"
        r = requests.post(register_url, json=user_data)
        return r.json()
