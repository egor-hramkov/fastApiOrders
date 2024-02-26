import pytest

from tests.items.item_utils import TestItem

CREATE_URL = "/items/create"
DELETE_URL = "/items/"


@pytest.fixture(scope="function")
def create_item(request, client):
    """
    Фикстура создания товара.
    Вызывается после каждой функции, создаёт товар и после логики тестовой функции - удаляет его
    """
    items = []

    def _create_item(item_data: dict) -> TestItem:
        response = client.post(CREATE_URL, json=item_data)
        assert response.status_code == 200
        item = response.json()
        items.append(item)
        return TestItem(**item)

    def delete_item():
        for item in items:
            response = client.delete(DELETE_URL + str(item['id']))
            assert response.status_code == 200

    request.addfinalizer(delete_item)
    return _create_item
