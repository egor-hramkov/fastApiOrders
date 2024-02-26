import pytest

from tests.orders.order_utils import TestOrder

CREATE_URL = "orders/create"
DELETE_URL = "orders/"


@pytest.fixture(scope="function")
def create_order(request, client, get_access_token):
    """
    Фикстура создания заказа.
    Вызывается после каждой функции, создаёт заказ и после логики тестовой функции - удаляет его
    """
    orders = []

    def _create_order(order_data: dict) -> TestOrder:
        access_token = get_access_token
        response = client.post(
            CREATE_URL,
            json=order_data,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        order = response.json()
        return TestOrder(**order)

    def delete_order():
        for order in orders:
            response = client.delete(DELETE_URL + str(order['id']))
            assert response.status_code == 200

    request.addfinalizer(delete_order)
    return _create_order
