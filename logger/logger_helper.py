import logging


def disable_3rd_party_logging():
    forbidden_loggers = [
        'kafka.coordinator.consumer',
        'kafka.coordinator',
        'kafka.consumer.subscription_state',
        'kafka.cluster',
        'kafka.conn',
    ]
    for logger in forbidden_loggers:
        logging.getLogger(logger).setLevel(logging.ERROR)
