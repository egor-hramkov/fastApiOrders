from sqlalchemy.exc import IntegrityError


class ExceptionParser:
    """Вспомогательный парсер для ошибок"""

    @staticmethod
    def parse_user_unique_exception(e: IntegrityError) -> str:
        """Получение значения, которое нарушает уникальность"""
        raw_exception: str = e.args[0]
        unique_fields = ['username', 'email']
        for field in unique_fields:
            if field in raw_exception:
                return field
