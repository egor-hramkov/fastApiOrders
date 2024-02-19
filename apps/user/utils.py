from sqlalchemy.exc import IntegrityError


class ExceptionParser:
    """Вспомогательный парсер для ошибок"""

    @staticmethod
    def parse_user_unique_exception(e: IntegrityError) -> str:
        """Получение значения, которое нарушает уникальность"""
        raw_exception: str = e.args[0]
        unique_fields = ['username', 'email', 'id']
        for field in unique_fields:
            if field in raw_exception:
                return field

    @staticmethod
    def parse_item_unique_exception(e: IntegrityError) -> str:
        """Получение значения, которое нарушает уникальность"""
        raw_exception: str = e.args[0]
        unique_fields = ['name']
        for field in unique_fields:
            if field in raw_exception:
                return field

    @staticmethod
    def parse_order_unique_exception(e: IntegrityError) -> str:
        """Получение значения, которое нарушает уникальность"""
        raw_exception: str = e.args[0]
        unique_fields = ['id']
        for field in unique_fields:
            if field in raw_exception:
                return field
