from sqlalchemy.exc import IntegrityError


class ExceptionParser:
    """Вспомогательный парсер для ошибок"""

    @staticmethod
    def parse_unique_exception(e: IntegrityError, unique_fields: list[str]) -> str | None:
        """Парсер значения, которое нарушает уникальность ключа БД"""
        raw_exception: str = e.args[0]
        for field in unique_fields:
            if field in raw_exception:
                return field
