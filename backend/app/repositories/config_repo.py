from sqlalchemy.orm import Session
from app.models.models import Config
from typing import Optional


class ConfigRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_by_key(self, key: str) -> Optional[Config]:
        """Pobiera konfigurację po kluczu"""
        return self.session.query(Config).filter(Config.CONF_Klucz == key).first()

    def get_value(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Pobiera wartość konfiguracji po kluczu (zwraca tylko wartość, nie cały obiekt)"""
        config = self.get_by_key(key)
        return config.CONF_Wartosc if config else default

    def get_all(self) -> list[Config]:
        """Pobiera wszystkie konfiguracje"""
        return self.session.query(Config).all()

    def set_value(self, key: str, value: str, opis: Optional[str] = None) -> Config:
        """Ustawia wartość konfiguracji (tworzy nową lub aktualizuje istniejącą)"""
        config = self.get_by_key(key)

        if config:
            # Aktualizuj istniejącą
            config.CONF_Wartosc = value
            if opis is not None:
                config.CONF_Opis = opis
        else:
            # Utwórz nową
            config = Config(
                CONF_Klucz=key,
                CONF_Wartosc=value,
                CONF_Opis=opis
            )
            self.session.add(config)

        self.session.commit()
        self.session.refresh(config)
        return config

    def delete(self, key: str) -> bool:
        """Usuwa konfigurację po kluczu"""
        config = self.get_by_key(key)
        if config:
            self.session.delete(config)
            self.session.commit()
            return True
        return False
