from sqlalchemy.types import TypeDecorator, NCHAR, CHAR, String
import sqlalchemy.types


class TrimmedString(TypeDecorator):
    """
    Typ, który automatycznie usuwa białe znaki z prawej strony (rstrip)
    przy każdym odczycie z bazy danych.

    Działa dla NCHAR, CHAR, VARCHAR, NVARCHAR itp.
    """
    impl = sqlalchemy.types.String
    cache_ok = True

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        # Jeśli wartość nie jest stringiem, skonwertuj ją najpierw
        if not isinstance(value, str):
            value = str(value)
        return value.rstrip()