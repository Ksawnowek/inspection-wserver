from app.repositories.config_repo import ConfigRepo
from app.models.models import Config
from typing import Optional


class ConfigService:
    """Serwis do zarządzania konfiguracją aplikacji"""

    # Klucze konfiguracji (stałe)
    KEY_ZDJECIA_SCIEZKA = "ZDJECIA_SCIEZKA"
    KEY_PDF_SCIEZKA = "PDF_SCIEZKA"

    def __init__(self, repo: ConfigRepo):
        self.repo = repo

    def get_config(self, key: str) -> Optional[Config]:
        """Pobiera konfigurację po kluczu"""
        return self.repo.get_by_key(key)

    def get_value(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Pobiera wartość konfiguracji"""
        return self.repo.get_value(key, default)

    def get_all_configs(self) -> list[Config]:
        """Pobiera wszystkie konfiguracje"""
        return self.repo.get_all()

    def set_config(self, key: str, value: str, opis: Optional[str] = None) -> Config:
        """Ustawia wartość konfiguracji"""
        return self.repo.set_value(key, value, opis)

    def delete_config(self, key: str) -> bool:
        """Usuwa konfigurację"""
        return self.repo.delete(key)

    # Pomocnicze metody dla często używanych konfiguracji
    def get_zdjecia_sciezka(self) -> str:
        """Pobiera ścieżkę do katalogu ze zdjęciami"""
        return self.repo.get_value(self.KEY_ZDJECIA_SCIEZKA, r"C:\Zdjecia\Protokoly")

    def set_zdjecia_sciezka(self, sciezka: str) -> Config:
        """Ustawia ścieżkę do katalogu ze zdjęciami"""
        return self.repo.set_value(
            self.KEY_ZDJECIA_SCIEZKA,
            sciezka,
            "Ścieżka do katalogu z zdjęciami protokołów"
        )

    def get_pdf_sciezka(self) -> str:
        """Pobiera ścieżkę do katalogu z PDF"""
        return self.repo.get_value(self.KEY_PDF_SCIEZKA, r"C:\PDF\Raporty")

    def set_pdf_sciezka(self, sciezka: str) -> Config:
        """Ustawia ścieżkę do katalogu z PDF"""
        return self.repo.set_value(
            self.KEY_PDF_SCIEZKA,
            sciezka,
            "Ścieżka do katalogu z raportami PDF"
        )
