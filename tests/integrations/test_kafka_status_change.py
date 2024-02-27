import json
import time

from kafka import KafkaProducer

from settings.kafka_settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from tests.integrations.conftest import MockConsumer
from tests.orders.conftest import create_order, get_order
from tests.orders.order_utils import get_test_order_create_data


class TestKafkaLayer:
    """Класс для тестирования статусов заказа"""
    order_data = get_test_order_create_data()

    def test_change_order_status(self, create_order, get_order):
        """Тест по изменению статуса заказа через Kafka"""
        new_order = create_order(self.order_data)
        assert new_order.status == 'created'

        with MockConsumer():
            self.send_msg_change_status(new_order.id)
            time.sleep(7)
        order = get_order(new_order.id)
        assert order.status == 'in_process'

    def send_msg_change_status(self, order_id: int, status: str = 'in_process') -> None:
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
            security_protocol="PLAINTEXT",
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        order = {
            'order_id': order_id,
            'status': status
        }
        producer.send(KAFKA_TOPIC, order)
        producer.flush()
