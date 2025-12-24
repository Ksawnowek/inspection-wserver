from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.dependencies import get_pdf_service, get_protokoly_service, any_logged_in_user
from app.services.PDF_service import PDFService
from app.services.protokoly_service import ProtokolyService
from app.models.models import Uzytkownik

router = APIRouter(prefix="/api/raporty", tags=["raporty"])


@router.post("/generuj/awaria/{znag_id}")
async def generuj_raport_awarii(
    znag_id: int,
    pdf_service: PDFService = Depends(get_pdf_service),
    current_user: Uzytkownik = Depends(any_logged_in_user)
):
    """Generuje raport PDF dla awarii."""
    try:
        # Pobierz nazwisko serwisanta z aktualnie zalogowanego użytkownika
        serwisant = f"{current_user.UZT_Imie} {current_user.UZT_Nazwisko}"

        pdf_path = pdf_service.generuj_pdf_zadania(znag_id, [serwisant])

        if not pdf_path.exists():
            raise HTTPException(status_code=500, detail="Nie udało się wygenerować PDF")

        return FileResponse(
            path=str(pdf_path),
            media_type="application/pdf",
            filename=f"awaria_{znag_id}.pdf"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd generowania raportu: {str(e)}")


@router.post("/generuj/prace_rozne/{znag_id}")
async def generuj_raport_prac_roznych(
    znag_id: int,
    pdf_service: PDFService = Depends(get_pdf_service),
    current_user: Uzytkownik = Depends(any_logged_in_user)
):
    """Generuje raport PDF dla prac różnych."""
    try:
        # Pobierz nazwisko serwisanta z aktualnie zalogowanego użytkownika
        serwisant = f"{current_user.UZT_Imie} {current_user.UZT_Nazwisko}"

        pdf_path = pdf_service.generuj_pdf_zadania(znag_id, [serwisant])

        if not pdf_path.exists():
            raise HTTPException(status_code=500, detail="Nie udało się wygenerować PDF")

        return FileResponse(
            path=str(pdf_path),
            media_type="application/pdf",
            filename=f"prace_rozne_{znag_id}.pdf"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd generowania raportu: {str(e)}")


@router.post("/generuj/konserwacja/{pnagl_id}")
async def generuj_raport_konserwacji(
    pnagl_id: int,
    pdf_service: PDFService = Depends(get_pdf_service),
    protokoly_service: ProtokolyService = Depends(get_protokoly_service),
    current_user: Uzytkownik = Depends(any_logged_in_user)
):
    """Generuje raport PDF dla protokołu konserwacji."""
    try:
        pdf_path = pdf_service.generuj_pdf_protokol(pnagl_id, protokoly_service)

        if not pdf_path.exists():
            raise HTTPException(status_code=500, detail="Nie udało się wygenerować PDF")

        return FileResponse(
            path=str(pdf_path),
            media_type="application/pdf",
            filename=f"konserwacja_{pnagl_id}.pdf"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd generowania raportu: {str(e)}")


@router.post("/generuj/montaz/{znag_id}")
async def generuj_raport_montazu(
    znag_id: int,
    pdf_service: PDFService = Depends(get_pdf_service),
    current_user: Uzytkownik = Depends(any_logged_in_user)
):
    """Generuje raport PDF dla montażu."""
    try:
        # Pobierz nazwisko serwisanta z aktualnie zalogowanego użytkownika
        serwisant = f"{current_user.UZT_Imie} {current_user.UZT_Nazwisko}"

        pdf_path = pdf_service.generuj_pdf_zadania(znag_id, [serwisant])

        if not pdf_path.exists():
            raise HTTPException(status_code=500, detail="Nie udało się wygenerować PDF")

        return FileResponse(
            path=str(pdf_path),
            media_type="application/pdf",
            filename=f"montaz_{znag_id}.pdf"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd generowania raportu: {str(e)}")
