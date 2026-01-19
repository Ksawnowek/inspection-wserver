from sqlalchemy.orm import Session
from app.models.models import Config


class ConfigRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_by_key(self, key: str) -> Config | None:
        """Pobiera konfigurację po kluczu"""
        return self.session.query(Config).filter(Config.CONF_Klucz == key).first()

    def get_value(self, key: str, default: str = None) -> str | None:
        """Pobiera wartość konfiguracji po kluczu"""
        config = self.get_by_key(key)
        if config:
            return config.CONF_Wartosc
        return default
