import pytest
from starlette.status import HTTP_200_OK

from tests.items.item_utils import get_test_item_data


class TestItem:
    """Тестовый класс для тестирования приложения товара"""
    CREATE_ITEM_URL = "items/create"
    GET_ITEM_URL = "items/"

    item_data = get_test_item_data()

    @pytest.mark.parametrize("create_item", [item_data], indirect=True)
    def test_create_item(self, create_item, client):
        """Тест создания товара"""
        assert create_item

    def test_create_item_with_wrong_price(self, client):
        """Тест создания товара с неправильной ценой"""
        item_data = {
            "name": "wrong item",
            "price": -120
        }
        response = client.post(self.CREATE_ITEM_URL, json=item_data)
        assert response.status_code == 422

    def test_get_item(self, create_item, client):
        """Тест получения товара"""
        item = create_item(self.item_data)
        response = client.get(self.GET_ITEM_URL + str(item.id))
        assert response.status_code == HTTP_200_OK
        assert response.json()['id'] == item.id
