from app.repositories.config_repo import ConfigRepo


class ConfigService:
    def __init__(self, repo: ConfigRepo):
        self.repo = repo

    def get_zdjecia_sciezka(self) -> str:
        """Pobiera ścieżkę do katalogu ze zdjęciami z konfiguracji"""
        # Klucz w bazie danych dla ścieżki do zdjęć
        sciezka = self.repo.get_value("ZDJECIA_SCIEZKA", "C:/Zdjecia/Protokoly")
        return sciezka

    def get_config_value(self, key: str, default: str = None) -> str | None:
        """Pobiera dowolną wartość konfiguracji po kluczu"""
        return self.repo.get_value(key, default)
