import os
import re
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
import shutil
console = Console()
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def save_page(url, carpeta_destino=None) -> str:
    url_meta = urlparse(url)
    carpeta_destino = carpeta_destino or url_meta.netloc
    download_site = os.path.join("www", carpeta_destino)
    if os.path.exists(download_site):
        shutil.rmtree(download_site)
    os.makedirs(download_site, exist_ok=True)

    # Usar Selenium para renderizar la página con JS
    console.print(f"[bold green]📡 Accediendo (renderizado JS) a:[/] {url}")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(5)  # esperar que JS cargue la página
        html_rendered = driver.page_source
        driver.quit()
    except Exception as e:
        console.print(f"[bold red]❌ Error al renderizar la página con Selenium:[/] {url} → {e}")
        return None

    soup = BeautifulSoup(html_rendered, "html.parser")

    # OPCIONAL: eliminar scripts peligrosos o innecesarios
    for script in soup.find_all("script", src=True):
        if "service-nologin.php" in script["src"] or "lib/ajax/service-nologin.php" in script["src"]:
            script.decompose()

    # Mapas de tag/atributo y carpetas de destino
    recursos = []
    tag_attr_folder = {
        "link":   ("href", "css"),
        "script": ("src",  "js"),
        "img":    ("src",  "images"),
        "source": ("src",  "media"),
        "video":  ("src",  "media"),
        "audio":  ("src",  "media"),
        "iframe": ("src",  "media")
    }

    for tag, (attr, subfolder) in tag_attr_folder.items():
        for tag_elem in soup.find_all(tag):
            if tag == "link" and tag_elem.get("rel") != ["stylesheet"]:
                continue
            if tag_elem.has_attr(attr):
                recurso_url = urljoin(url, tag_elem[attr])
                recursos.append((tag_elem, attr, recurso_url, subfolder))

    console.print(f"[bold cyan]🎯 Recursos a descargar:[/] {len(recursos)}")

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TimeElapsedColumn(), console=console) as progress:
        tarea = progress.add_task("Descargando recursos...", total=len(recursos))

        for tag_elem, attr, recurso_url, subfolder in recursos:
            nombre_archivo = os.path.basename(urlparse(recurso_url).path)
            if not nombre_archivo or "." not in nombre_archivo:
                nombre_archivo = re.sub(r'\W+', '_', recurso_url.split("/")[-1]) or "recurso"
                nombre_archivo += ".bin"

            ruta_carpeta = os.path.join(download_site, subfolder)
            os.makedirs(ruta_carpeta, exist_ok=True)
            ruta_local = os.path.join(ruta_carpeta, nombre_archivo)

            try:
                r = requests.get(recurso_url, timeout=5)
                with open(ruta_local, "wb") as f:
                    f.write(r.content)
                tag_elem[attr] = os.path.relpath(ruta_local, start=download_site)
            except Exception as e:
                console.print(f"[yellow]⚠️ No se pudo descargar {recurso_url}[/]: {e}")

            progress.advance(tarea)

    for tag in soup.find_all(style=True):
        estilo = tag["style"]
        urls = re.findall(r'url\((.*?)\)', estilo)
        for u in urls:
            limpio = u.strip('"\'')
            abs_url = urljoin(url, limpio)
            nombre_archivo = os.path.basename(urlparse(abs_url).path) or "fondo.jpg"
            ruta_img = os.path.join(download_site, "images", nombre_archivo)

            try:
                r = requests.get(abs_url, timeout=5)
                with open(ruta_img, "wb") as f:
                    f.write(r.content)
                local_path = os.path.relpath(ruta_img, start=download_site)
                estilo = estilo.replace(limpio, local_path)
            except:
                continue
        tag["style"] = estilo

    ruta_html = os.path.join(download_site, "index.html")
    with open(ruta_html, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    console.print(f"\n[bold green]✅ Página guardada correctamente en:[/] {ruta_html}")
    return os.path.abspath(download_site)
