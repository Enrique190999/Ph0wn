import os
import socket
import threading
import http.server
import socketserver
import webbrowser
from rich.console import Console

console = Console()

def obtener_ip_local():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") or ip.startswith("0."):
        # fallback por DHCP (Google DNS)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
    return ip

def start_socket_web(project_deploy, index_item="index.html", port=8000):
    project_deploy = os.path.join('www',project_deploy)
    os.chdir(project_deploy)
    ip_local = obtener_ip_local()

    def run():
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
            console.print(f"[bold green]🌐 Servidor web en:[/] http://{ip_local}:{port}/{index_item}")
            console.print(f"[dim]Accesible desde otros dispositivos en la red local[/]")
            httpd.serve_forever()

    hilo = threading.Thread(target=run, daemon=True)
    hilo.start()

    try:
        webbrowser.open(f"http://localhost:{port}/{index_item}")
    except:
        pass

    input("🔁 Pulsa ENTER para detener el servidor...\n")
