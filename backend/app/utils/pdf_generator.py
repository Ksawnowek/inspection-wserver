import base64
import mimetypes
import os
import shutil
from pathlib import Path
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import sync_playwright

from app.models.models import ProtokolPoz, ProtokolNagl, ZadanieNagl, ZadaniePoz, ZadanieInneOpis, ZadanieInneMaterial

# Ścieżki
TEMPL_DIR = Path(__file__).resolve().parent.parent / "templates"
LOGO_PATH = Path(__file__).resolve().parent.parent / "static" / "images" / "logo.png"

# Konfiguracja Jinja2 (Poprawione wcięcia)
env = Environment(
    loader=FileSystemLoader(str(TEMPL_DIR)),
    autoescape=select_autoescape(["html", "xml"])
)

def get_logo_url():
    """
    Zamiast ścieżki pliku, zwraca obrazek zakodowany w Base64.
    Dzięki temu działa wszędzie (lokalnie, usługa, docker) i omija problemy z uprawnieniami plików.
    """
    if LOGO_PATH.exists():
        try:
            # Otwieramy plik w trybie binarnym
            with open(LOGO_PATH, "rb") as img_file:
                # Kodujemy do base64 i dekodujemy na string (utf-8)
                encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
                
                # Sprawdzamy typ pliku (png/jpg)
                mime_type, _ = mimetypes.guess_type(LOGO_PATH)
                if not mime_type:
                    mime_type = "image/png" # Domyślnie
                
                # Zwracamy gotowy string Data URI do wstawienia w src=""
                return f"data:{mime_type};base64,{encoded_string}"
        except Exception as e:
            print(f"Błąd ładowania logo: {e}")
            return ""
            
    return ""

def generate_pdf_with_playwright(html_content: str, output_path: str):
    """
    Generuje PDF z HTML używając Playwright (Chromium).
    Zawiera fixy dla Windows Service (LocalSystem) oraz renderowania CSS.
    """
    # 1. Tworzymy tymczasowy profil, bo Usługa Windows (LocalSystem) nie ma swojego katalogu domowego
    # Bez tego Playwright wywali błąd zapisu profilu
    temp_dir = os.path.abspath(f"temp_pw_profile_{datetime.now().timestamp()}")
    os.makedirs(temp_dir, exist_ok=True)

    browser = None
    try:
        with sync_playwright() as p:
            # Używamy launch_persistent_context dla stabilności w usługach
            browser = p.chromium.launch_persistent_context(
                user_data_dir=temp_dir,
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-gpu",
                    "--disable-dev-shm-usage"
                ]
            )
            
            page = browser.new_page()

            # Załaduj HTML
            page.set_content(html_content, wait_until="networkidle")
            
            # WAŻNE: Wymuszamy media="screen", żeby CSS drukarkowe nie psuły wyglądu (tła, kolory)
            page.emulate_media(media="screen")

            # Wygeneruj PDF
            page.pdf(
                path=output_path,
                format="A4",
                print_background=True,
                margin={
                    "top": "10mm",
                    "bottom": "10mm",
                    "left": "10mm",
                    "right": "10mm"
                }
            )
            
            browser.close()
            browser = None

    except Exception as e:
        # Rzucamy wyjątek dalej, żeby API wiedziało, że coś poszło nie tak
        raise e
    finally:
        # Sprzątanie: zamykamy przeglądarkę jeśli otwarta i usuwamy folder temp
        if browser:
            try: browser.close()
            except: pass
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass

def render_zadanie_pdf(out_path: str, naglowek: ZadanieNagl, podpis: str, pozycje: list[ZadaniePoz], serwisanci: list[str] | None = None):
    """Wyrenderuj HTML z Jinja2 i zapisz jako PDF przez Playwright."""
    serwisanci = serwisanci or []
    
    html = env.get_template("zadanie.html").render(
        today=datetime.now().strftime("%d-%m-%Y"),
        naglowek=naglowek,
        podpis_klient=podpis,
        pozycje=pozycje,
        serwisanci=serwisanci,
        logo_url=get_logo_url()
    )

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    generate_pdf_with_playwright(html, str(out))

    return str(out)

def render_awaria_pdf(out_path: str, naglowek: ZadanieNagl, podpis: str, pozycje: list[ZadaniePoz], serwisanci: list[str] | None = None, opis_prac: list[ZadanieInneOpis] | None = None, materialy: list[dict] | None = None):
    """Wyrenderuj HTML z Jinja2 i zapisz jako PDF przez Playwright dla zadań typu awaria."""
    serwisanci = serwisanci or []
    opis_prac = opis_prac or []
    materialy = materialy or []
    
    html = env.get_template("awaria.html").render(
        today=datetime.now().strftime("%d-%m-%Y"),
        naglowek=naglowek,
        podpis_klient=podpis,
        pozycje=pozycje,
        serwisanci=serwisanci,
        opis_prac=opis_prac,
        materialy=materialy,
        logo_url=get_logo_url()
    )

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    generate_pdf_with_playwright(html, str(out))

    return str(out)

def render_prace_rozne_pdf(out_path: str, naglowek: ZadanieNagl, podpis: str, pozycje: list[ZadaniePoz], serwisanci: list[str] | None = None, opis_prac: list[ZadanieInneOpis] | None = None, materialy: list[dict] | None = None):
    """Wyrenderuj HTML z Jinja2 i zapisz jako PDF przez Playwright dla zadań typu prace różne."""
    serwisanci = serwisanci or []
    opis_prac = opis_prac or []
    materialy = materialy or []
    
    html = env.get_template("prace_rozne.html").render(
        today=datetime.now().strftime("%d-%m-%Y"),
        naglowek=naglowek,
        podpis_klient=podpis,
        pozycje=pozycje,
        serwisanci=serwisanci,
        opis_prac=opis_prac,
        materialy=materialy,
        logo_url=get_logo_url()
    )

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    generate_pdf_with_playwright(html, str(out))

    return str(out)

def render_protokol_pdf(out_path: str, protokol_nagl: ProtokolNagl, zadanie_nagl: ZadanieNagl, protokol_grupy: list[dict] | None = None):
    """Generuje protokół"""
    html = env.get_template("protokol.html").render(
        today=datetime.now().strftime("%d-%m-%Y"),
        naglowek_zadanie=zadanie_nagl,
        naglowek_protokol=protokol_nagl,
        protokol_grupy=protokol_grupy,
        logo_url=get_logo_url()
    )

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    generate_pdf_with_playwright(html, str(out))

    return str(out)