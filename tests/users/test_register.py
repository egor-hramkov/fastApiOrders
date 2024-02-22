from starlette.status import HTTP_200_OK


class TestUserRegister:
    """Класс для тестирования регистрации пользователя"""
    REGISTER_URL = "/user/register"
    user_data = {
        "username": "string",
        "email": "user@example.com",
        "name": "string",
        "surname": "string",
        "father_name": "string",
        "password": "string"
    }

    def test_register(self, client):
        response = client.post(self.REGISTER_URL, json=self.user_data)
        assert response.status_code == HTTP_200_OK
        user = response.json()
        assert user
        assert user['username'] == self.user_data["username"]
