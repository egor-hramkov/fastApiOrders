import pytest

from tests.users.users_utils import TestUser

REGISTER_URL = "/user/register"
DELETE_URL = "/user/"


@pytest.fixture(scope="function")
def create_user(request, client) -> TestUser:
    """Фикстура создания пользователя"""
    user_data = request.param
    response = client.post(REGISTER_URL, json=user_data)
    assert response.status_code == 200
    user = response.json()
    yield TestUser(**user)
    response = client.delete(DELETE_URL + str(user['id']))
    assert response.status_code == 200
