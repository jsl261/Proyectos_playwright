import pytest
from playwright.sync_api import sync_playwright


def test_google_sin_captcha():
    with sync_playwright() as p:
        # Ruta a tu carpeta de datos creada en el paso 1
        user_data_dir = "./user_data"
        
        # Lanzamos el navegador persistente (Usa tu Chrome de Kubuntu)
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"] # TRUCO CLAVE
        )
        
        page = context.pages[0]
        page.goto("https://www.google.com")

        # --- INTERVENCIÓN HUMANA SI ES NECESARIO ---
        # Si la primera vez te sale el CAPTCHA, resuélvelo MANUELA MENTE.
        # Gracias al 'user_data_dir', Google recordará que ya lo resolviste
        # y no te lo pedirá en las siguientes ejecuciones.
        
        search_bar = page.locator('xpath=//textarea[@name="q"] | //input[@name="q"]')
        search_bar.fill("mejor inteligencia artificial para QA")
        search_bar.press("Enter")
        
        page.wait_for_selector("#search", timeout=10000)
        print(f"Título: {page.title()}")
        
        # No cerramos el contexto inmediatamente para ver el resultado
        page.wait_for_timeout(3000)
        context.close()