import concurrent.futures as pool
from multiprocessing import Process

from kafka_layer.consumer.consumer_listener import run_consumer


class MockConsumer:
    """Включает kafka consumer"""

    def __enter__(self):
        self.process = Process(target=run_consumer)
        self.process.start()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.process.terminate()
