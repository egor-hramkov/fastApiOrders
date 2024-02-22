import pytest
from starlette.status import HTTP_200_OK

from tests.users.users_utils import get_test_user_data


class TestUserAuth:
    """Класс для тестирования авторизации пользователя"""
    URL_OAUTH = '/auth/token'
    user_data = get_test_user_data()

    @pytest.mark.parametrize("create_user", [user_data], indirect=True)
    def test_user_auth(self, client, create_user):
        """Тест авторизации пользователя"""
        user = create_user
        data = {
            "username": user.username,
            "password": self.user_data['password']
        }
        response = client.post(self.URL_OAUTH, data=data)
        print(response)
        print(response.json())
        assert response.status_code == HTTP_200_OK
        assert response.json().get('access_token')
