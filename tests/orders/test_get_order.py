from starlette.status import HTTP_200_OK

from tests.orders.order_utils import get_test_order_create_data


class TestGetOrder:
    """Тест на получение заказов"""
    GET_ORDER_URL = "orders/"
    order_data = get_test_order_create_data()

    def test_get_order(self, client, create_order, get_access_token):
        """Тест на получение заказа"""
        new_order = create_order(self.order_data)
        response = client.get(
            self.GET_ORDER_URL + str(new_order.id),
            headers={"Authorization": f"Bearer {get_access_token}"}
        )
        assert response.status_code == HTTP_200_OK
        assert response.json()['id'] == new_order.id
