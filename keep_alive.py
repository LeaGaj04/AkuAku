import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"Aku Aku bot is online and running 24/7!")

    def log_message(self, format, *args):
        # Silenciar logs HTTP periódicos de health check
        return

def run_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

def keep_alive():
    """Inicia un servidor HTTP ligero en segundo plano para pasar los health checks de Koyeb."""
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
