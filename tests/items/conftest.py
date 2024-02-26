import pytest

from tests.items.item_utils import TestItem

CREATE_URL = "/items/create"
DELETE_URL = "/items/"


@pytest.fixture(scope="function")
def create_item(request, client) -> TestItem:
    """
    Фикстура создания товара.
    Вызывается после каждой функции, создаёт товар и после логики тестовой функции - удаляет его
    """
    item_data = request.param
    response = client.post(CREATE_URL, json=item_data)
    assert response.status_code == 200
    item = response.json()
    yield TestItem(**item)
    response = client.delete(DELETE_URL + str(item['id']))
    assert response.status_code == 200
