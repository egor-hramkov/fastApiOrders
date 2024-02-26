from fastapi.testclient import TestClient
import os
import pytest
from dotenv import load_dotenv
from alembic import command, config
from starlette.status import HTTP_200_OK

from main import app

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
migration_path = os.path.join(ROOT_DIR, 'migrations')
alembic_path = os.path.join(ROOT_DIR, 'alembic.ini')


@pytest.fixture(scope="session", autouse=True)
def apply_migrations_to_db():
    """Применяет миграции к БД"""
    assert os.environ.get('MODE') == 'TEST'
    database_name = os.environ.get('db_name')
    alembic_config = config.Config(alembic_path)
    alembic_config.set_main_option("script_location", migration_path)
    alembic_config.set_main_option("sqlalchemy.url", database_name)
    command.upgrade(alembic_config, "head")
    yield
    command.downgrade(alembic_config, "base")


@pytest.fixture(scope="session", autouse=True)
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def create_test_user(client):
    """Создаёт тестового пользователя для тестовой сессии"""
    REGISTER_URL = "user/register/"
    DELETE_URL = "/user/"

    user_data = {
        "username": "main_test_user",
        "email": "main_test_user@example.com",
        "name": "main_test_user",
        "surname": "main_test_user",
        "father_name": "main_test_user",
        "password": "main_test_user"
    }
    response = client.post(REGISTER_URL, json=user_data)
    assert response.status_code == 200
    user = response.json()
    yield
    response = client.delete(DELETE_URL + str(user['id']))
    assert response.status_code == 200


@pytest.fixture
def get_access_token(client):
    """Получает access token готового авторизованного пользователя"""
    URL_OAUTH = '/auth/token'

    data = {
        "username": "main_test_user",
        "password": "main_test_user"
    }
    response = client.post(URL_OAUTH, data=data)
    assert response.status_code == HTTP_200_OK
    return response.json()['access_token']
