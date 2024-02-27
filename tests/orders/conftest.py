import pytest

from tests.orders.order_utils import TestOrder

CREATE_URL = "orders/create"
DELETE_URL = "orders/"
GET_ORDER_URL = "orders/"


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
        orders.append(order)
        return TestOrder(**order)

    def delete_order():
        for order in orders:
            response = client.delete(
                DELETE_URL + str(order['id']),
                headers={"Authorization": f"Bearer {get_access_token}"}
            )
            assert response.status_code == 200

    request.addfinalizer(delete_order)
    return _create_order


@pytest.fixture(scope="function")
def get_order(request, client, get_access_token):
    def _get_order(order_id: int) -> TestOrder:
        response = client.get(
            GET_ORDER_URL + str(order_id),
            headers={"Authorization": f"Bearer {get_access_token}"}
        )
        assert response.status_code == 200
        order = response.json()
        return TestOrder(**order)

    return _get_order
