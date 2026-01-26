import os
import uuid
import aiofiles
from pathlib import Path

from fastapi import HTTPException

from app.repositories.zdjecia_repo import ZdjeciaRepo
from app.services.config_service import ConfigService


class ZdjeciaService:
    def __init__(self, repo: ZdjeciaRepo, config_service: ConfigService):
        self.repo = repo
        self.config_service = config_service

    def _get_photo_dir(self) -> Path:
        """Pobiera ścieżkę do katalogu ze zdjęciami z konfiguracji w bazie danych"""
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

        # Zapisz tylko nazwę pliku do bazy danych
        # Ścieżka katalogu jest w konfiguracji (ZDJECIA_SCIEZKA)
        zdjecie = self.repo.dodaj_zdjecie(ppoz_id, safe_filename)
        self.repo.session.commit()
        self.repo.session.refresh(zdjecie)

        return zdjecie

    def get_zdjecie_file_path(self, zdjp_id: int) -> Path:
        """Pobiera fizyczną ścieżkę do pliku zdjęcia"""
        zdjecie = self.repo.get_pozycja_zdjecie_by_id(zdjp_id)

        if zdjecie is None:
            raise HTTPException(status_code=404, detail="Nie znaleziono zdjęcia o podanym ID")

        path_str = zdjecie.ZDJP_Sciezka

        # Pobierz katalog ze zdjęciami z konfiguracji
        photo_dir = Path(self.config_service.get_zdjecia_sciezka())

        # Obsługa różnych formatów ścieżek (kompatybilność wsteczna)
        if path_str.startswith('/') or path_str.startswith('\\'):
            # Stary format URL lub ścieżki - wyciągnij tylko nazwę pliku
            filename = path_str.split('/')[-1].split('\\')[-1]
            file_path = photo_dir / filename
        elif ':' in path_str and len(path_str) > 2:
            # Pełna ścieżka Windows (np. C:\...) - wyciągnij tylko nazwę pliku
            filename = Path(path_str).name
            file_path = photo_dir / filename
        else:
            # Nowy format - tylko nazwa pliku
            file_path = photo_dir / path_str

        # Sprawdź czy plik istnieje
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"Plik nie istnieje: {file_path}")

        return file_path

    def delete_pozycja_zdjecie(self, zdjp_id: int):
        zdjecie = self.repo.get_pozycja_zdjecie_by_id(zdjp_id)

        if zdjecie is None:
            raise HTTPException(status_code=404, detail="Nie znaleziono zdjęcia o podanym ID")

        # Pobierz fizyczną ścieżkę do pliku
        try:
            file_path_to_delete = self.get_zdjecie_file_path(zdjp_id)
        except HTTPException:
            # Plik nie istnieje na dysku - kontynuuj usuwanie z bazy
            file_path_to_delete = None

        # Usuń plik z dysku (jeśli istnieje)
        if file_path_to_delete and file_path_to_delete.exists():
            try:
                os.remove(file_path_to_delete)
            except Exception as e:
                print(f"BŁĄD: Nie udało się usunąć pliku {file_path_to_delete}: {e}")
                raise HTTPException(status_code=500, detail="Błąd podczas usuwania pliku z dysku.")

        # Usuń rekord z bazy danych
        self.repo.delete_zdjecie(zdjecie)
        self.repo.session.commit()

        return True
