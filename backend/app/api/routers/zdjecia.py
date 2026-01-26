from pathlib import Path
import mimetypes

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Response, status
from fastapi.responses import FileResponse

from app.dependencies import get_zdjecia_service, any_logged_in_user, get_zdjecia_repo
from app.models.models import Uzytkownik
from app.services.zdjecia_service import ZdjeciaService
from app.repositories.zdjecia_repo import ZdjeciaRepo

router = APIRouter(prefix="/api/zdjecia", tags=["Zdjecia"])

@router.post("/pozycja/{ppoz_id}")
async def post_pozycja_zdjecie(
        ppoz_id: int,
        file: UploadFile = File(...),
        service: ZdjeciaService = Depends(get_zdjecia_service),
        user: Uzytkownik = Depends(any_logged_in_user)
    ):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Dozwolone są tylko pliki obrazów")
    return await service.add_pozycja_zdjecie(ppoz_id, file)


@router.get("/view/{zdjp_id}")
def get_zdjecie_file(
        zdjp_id: int,
        service: ZdjeciaService = Depends(get_zdjecia_service),
        user: Uzytkownik = Depends(any_logged_in_user)
    ):
    """Zwraca plik zdjęcia (streamowanie przez API)"""
    file_path = service.get_zdjecie_file_path(zdjp_id)
    return FileResponse(file_path)


@router.delete("/pozycja/{zdjp_id}")
def delete_pozycja_zdjecie(
        zdjp_id: int,
        service: ZdjeciaService = Depends(get_zdjecia_service),
        user: Uzytkownik = Depends(any_logged_in_user)
    ):
    service.delete_pozycja_zdjecie(zdjp_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/file/{zdjp_id}")
def get_zdjecie_file_by_id(
        zdjp_id: int,
        service: ZdjeciaService = Depends(get_zdjecia_service),
        user: Uzytkownik = Depends(any_logged_in_user)
    ):
    """Serwuje plik zdjęcia na podstawie ID z bazy danych (z obsługą różnych formatów ścieżek)"""
    file_path = service.get_zdjecie_file_path(zdjp_id)

    # Wykryj typ MIME na podstawie rozszerzenia
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type is None:
        mime_type = "application/octet-stream"

    return FileResponse(
        path=file_path,
        media_type=mime_type,
        filename=file_path.name
    )
