from fastapi import APIRouter, Depends, HTTPException
from app.services.config_service import ConfigService
from app.dependencies import get_config_service, kierownik_only, any_logged_in_user
from app.models.models import Uzytkownik, Config
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/config", tags=["config"])


class ConfigUpdateDTO(BaseModel):
    """DTO do aktualizacji konfiguracji"""
    wartosc: str
    opis: Optional[str] = None


class ConfigResponseDTO(BaseModel):
    """DTO odpowiedzi z konfiguracją"""
    klucz: str
    wartosc: Optional[str]
    opis: Optional[str]

    class Config:
        from_attributes = True


@router.get("/", response_model=list[ConfigResponseDTO])
def get_all_configs(
    service: ConfigService = Depends(get_config_service),
    user: Uzytkownik = Depends(kierownik_only)
):
    """
    Pobiera wszystkie konfiguracje (tylko dla koordynatora)
    """
    configs = service.get_all_configs()
    return [
        ConfigResponseDTO(
            klucz=c.CONF_Klucz,
            wartosc=c.CONF_Wartosc,
            opis=c.CONF_Opis
        )
        for c in configs
    ]


@router.get("/{key}", response_model=ConfigResponseDTO)
def get_config(
    key: str,
    service: ConfigService = Depends(get_config_service),
    user: Uzytkownik = Depends(any_logged_in_user)
):
    """
    Pobiera konfigurację po kluczu
    """
    config = service.get_config(key)
    if not config:
        raise HTTPException(status_code=404, detail=f"Konfiguracja '{key}' nie istnieje")

    return ConfigResponseDTO(
        klucz=config.CONF_Klucz,
        wartosc=config.CONF_Wartosc,
        opis=config.CONF_Opis
    )


@router.put("/{key}", response_model=ConfigResponseDTO)
def update_config(
    key: str,
    dto: ConfigUpdateDTO,
    service: ConfigService = Depends(get_config_service),
    user: Uzytkownik = Depends(kierownik_only)
):
    """
    Aktualizuje konfigurację (tylko dla koordynatora)
    """
    try:
        config = service.set_config(key, dto.wartosc, dto.opis)
        return ConfigResponseDTO(
            klucz=config.CONF_Klucz,
            wartosc=config.CONF_Wartosc,
            opis=config.CONF_Opis
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{key}")
def delete_config(
    key: str,
    service: ConfigService = Depends(get_config_service),
    user: Uzytkownik = Depends(kierownik_only)
):
    """
    Usuwa konfigurację (tylko dla koordynatora)
    """
    if not service.delete_config(key):
        raise HTTPException(status_code=404, detail=f"Konfiguracja '{key}' nie istnieje")

    return {"ok": True, "message": f"Konfiguracja '{key}' została usunięta"}


# Pomocnicze endpointy dla często używanych konfiguracji

@router.get("/paths/zdjecia")
def get_zdjecia_path(
    service: ConfigService = Depends(get_config_service),
    user: Uzytkownik = Depends(any_logged_in_user)
):
    """
    Pobiera ścieżkę do katalogu ze zdjęciami
    """
    return {"sciezka": service.get_zdjecia_sciezka()}


@router.put("/paths/zdjecia")
def update_zdjecia_path(
    dto: ConfigUpdateDTO,
    service: ConfigService = Depends(get_config_service),
    user: Uzytkownik = Depends(kierownik_only)
):
    """
    Aktualizuje ścieżkę do katalogu ze zdjęciami (tylko dla koordynatora)
    """
    try:
        service.set_zdjecia_sciezka(dto.wartosc)
        return {"ok": True, "sciezka": dto.wartosc}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/paths/pdf")
def get_pdf_path(
    service: ConfigService = Depends(get_config_service),
    user: Uzytkownik = Depends(any_logged_in_user)
):
    """
    Pobiera ścieżkę do katalogu z PDF
    """
    return {"sciezka": service.get_pdf_sciezka()}


@router.put("/paths/pdf")
def update_pdf_path(
    dto: ConfigUpdateDTO,
    service: ConfigService = Depends(get_config_service),
    user: Uzytkownik = Depends(kierownik_only)
):
    """
    Aktualizuje ścieżkę do katalogu z PDF (tylko dla koordynatora)
    """
    try:
        service.set_pdf_sciezka(dto.wartosc)
        return {"ok": True, "sciezka": dto.wartosc}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
