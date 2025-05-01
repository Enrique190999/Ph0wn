def choose_index_item(path_web,is_mod=False):import os
from urllib.parse import urlparse
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import os

console = Console()

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import os

console = Console()

def choose_web():
    carpeta = 'www'

    if not os.path.exists(carpeta):
        console.print(f"[bold red]❌ La ruta no existe:[/] {carpeta}")
        return None

    carpetas = [d for d in os.listdir(carpeta) if os.path.isdir(os.path.join(carpeta, d))]
    
    if not carpetas:
        console.print(f"[yellow]⚠️ No hay páginas descargadas en:[/] {carpeta}")
        return None

    # Mostrar carpetas en tabla bonita
    table = Table(title="Proyectos de páginas descargadas")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Nombre de Carpeta", style="magenta")

    for i, carpeta_nombre in enumerate(carpetas):
        table.add_row(str(i), carpeta_nombre)

    console.print(table)

    # Selección del usuario
    seleccion = Prompt.ask("Selecciona el ID del proyecto", choices=[str(i) for i in range(len(carpetas))])
    carpeta_elegida = carpetas[int(seleccion)]

    console.print(f"[bold green]✔️ Proyecto seleccionado:[/] {carpeta_elegida}")

    return carpeta_elegida

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import os

console = Console()

def choose_index_item(path_web):
    carpeta = os.path.join("www", path_web)

    if not os.path.exists(carpeta):
        console.print(f"[bold red]❌ La ruta no existe:[/] {carpeta}")
        return None

    archivos = [f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]

    if not archivos:
        console.print(f"[yellow]⚠️ No hay archivos en la carpeta:[/] {carpeta}")
        return None

    # Mostrar archivos en tabla bonita
    table = Table(title=f"Archivos en {carpeta}")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Nombre de Archivo", style="magenta")

    for i, archivo in enumerate(archivos):
        table.add_row(str(i), archivo)

    console.print(table)

    seleccion = Prompt.ask("Selecciona el ID del archivo", choices=[str(i) for i in range(len(archivos))])
    archivo_elegido = archivos[int(seleccion)]

    console.print(f"[bold green]✔️ Archivo seleccionado:[/] {archivo_elegido}")

    return archivo_elegido
