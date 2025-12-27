import os
import uuid
import aiofiles
import asyncio
from pathlib import Path

from fastapi import HTTPException

from app.repositories.zdjecia_repo import ZdjeciaRepo
from app.services.config_service import ConfigService


class ZdjeciaService:
    def __init__(self, repo: ZdjeciaRepo, config_service: ConfigService):
        self.repo = repo
        self.config_service = config_service

    def _get_photo_dir(self) -> Path:
        """Pobiera ścieżkę do katalogu ze zdjęciami z konfiguracji"""
        sciezka = self.config_service.get_zdjecia_sciezka()
        photo_dir = Path(sciezka)
        photo_dir.mkdir(parents=True, exist_ok=True)
        return photo_dir

    async def add_pozycja_zdjecie(self, ppoz_id, file):
        photo_dir = self._get_photo_dir()

        file_ext = os.path.splitext(file.filename)[1]
        safe_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = photo_dir / safe_filename

        try:
            async with aiofiles.open(file_path, "wb") as out_file:
                content = await file.read()
                await out_file.write(content)
        except Exception as e:
            print(f"BŁĄD REPOZYTORIUM: Nie udało się zapisać pliku {file_path}: {e}")
            raise HTTPException(status_code=500, detail="Błąd zapisu pliku na serwerze")

        # Zapisz pełną ścieżkę do bazy danych
        file_url = str(file_path)

        zdjecie = self.repo.dodaj_zdjecie(ppoz_id, file_url)

        return zdjecie

    def delete_pozycja_zdjecie(self, zdjp_id: int):
        zdjecie = self.repo.get_pozycja_zdjecie_by_id(zdjp_id)

        if zdjecie is None:
            raise HTTPException(status_code=404, detail="Nie znaleziono zdjęcia o podanym ID")

        try:
            file_path_to_delete = Path(zdjecie.ZDJP_Sciezka)
        except Exception as e:
            print(f"BŁĄD: Nie można ustalić ścieżki pliku dla {zdjecie.ZDJP_Sciezka}: {e}")
            raise HTTPException(status_code=500, detail="Błąd przetwarzania ścieżki pliku")

        try:
            os.remove(file_path_to_delete)
        except FileNotFoundError:
            print(f"OSTRZEŻENIE: Próbowano usunąć plik, którego nie ma na dysku: {file_path_to_delete}")
        except Exception as e:
            print(f"BŁĄD: Nie udało się usunąć pliku {file_path_to_delete}: {e}")
            raise HTTPException(status_code=500, detail=f"Błąd podczas usuwania pliku z dysku.")

        self.repo.delete_zdjecie(zdjecie)

        return True

