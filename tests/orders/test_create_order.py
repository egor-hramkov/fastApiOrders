from starlette.status import HTTP_200_OK

from tests.items.conftest import create_item
from tests.orders.order_utils import get_test_order_create_data


class TestCreateOrder:
    """Тест создания заказа"""
    CREATE_URL = "orders/create"
    items_data = {
        "item_1": {
            "name": "test item",
            "price": 100
        },
        "item_2": {
            "name": "test item 2",
            "price": 200
        }
    }

    order_data = get_test_order_create_data()

    def test_create_order(self, create_item, get_access_token, client):
        """Тест создания заказа """
        item1 = create_item(self.items_data['item_1'])
        item2 = create_item(self.items_data['item_2'])
        access_token = get_access_token
        response = client.post(
            self.CREATE_URL,
            json=self.order_data,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        print(response.json())
        assert response.status_code == HTTP_200_OK
        order_id = response.json()['id']
        order_status = response.json()['status']
        assert order_id
        assert order_status == 'created'
