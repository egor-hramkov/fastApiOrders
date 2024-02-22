from fastapi.testclient import TestClient
import os
import pytest
from dotenv import load_dotenv
from alembic import command, config

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


@pytest.fixture(scope="session", autouse=True)
def client() -> TestClient:
    return TestClient(app)
