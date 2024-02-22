import pytest
from starlette.status import HTTP_200_OK

from tests.users.users_utils import TestUser, get_test_user_data


class TestUserGetting:
    """Класс для тестирования API получения пользователя"""
    GET_USER_URL = "/user/"
    GET_ALL_USERS_URL = "/user/all"

    @pytest.mark.parametrize("create_user", [get_test_user_data()], indirect=True)
    def test_get_user(self, client, create_user):
        """Тест получения пользователя"""
        user: TestUser = create_user
        print(f"USER: {user}")
        response = client.get(self.GET_USER_URL + str(user.id))
        response_user = response.json()
        assert response.status_code == HTTP_200_OK
        assert response_user["username"] == user.username
        assert response_user["id"] == user.id

    @pytest.mark.parametrize("create_user", [get_test_user_data()], indirect=True)
    def test_get_all_users(self, client, create_user):
        """Тест получения всех пользователей"""
        user1: TestUser = create_user
        response = client.get(self.GET_ALL_USERS_URL)
        users = response.json()
        assert response.status_code == HTTP_200_OK
        assert len(users) > 0
