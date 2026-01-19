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

        # Zapisz relatywny URL do bazy danych (zamiast pełnej ścieżki systemowej)
        # Konwertuj np. C:\storage\photos\abc.jpg -> /storage/photos/abc.jpg
        relative_path = file_path.relative_to(photo_dir.parent)
        file_url = "/" + str(relative_path).replace("\\", "/")

        zdjecie = self.repo.dodaj_zdjecie(ppoz_id, file_url)
        self.repo.session.commit()
        self.repo.session.refresh(zdjecie)

        # Upewnij się że ścieżka jest znormalizowana przy zwracaniu
        zdjecie.ZDJP_Sciezka = zdjecie._normalize_path()

        return zdjecie

    def delete_pozycja_zdjecie(self, zdjp_id: int):
        zdjecie = self.repo.get_pozycja_zdjecie_by_id(zdjp_id)

        if zdjecie is None:
            raise HTTPException(status_code=404, detail="Nie znaleziono zdjęcia o podanym ID")

        # Konwertuj ścieżkę z URL lub pełnej ścieżki systemowej na fizyczną ścieżkę do pliku
        try:
            path_str = zdjecie.ZDJP_Sciezka

            # Jeśli to URL (zaczyna się od /), konwertuj na ścieżkę systemową
            if path_str.startswith('/'):
                # /storage/photos/abc.jpg -> STORAGE_DIR/photos/abc.jpg
                relative_to_storage = path_str.lstrip('/').split('/', 1)[1]  # photos/abc.jpg
                photo_dir = self._get_photo_dir()
                file_path_to_delete = photo_dir / relative_to_storage
            else:
                # Stara pełna ścieżka systemowa
                file_path_to_delete = Path(path_str)

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

