import os
import time
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from pyngrok import ngrok

BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

PORT = 8000
LINK_FILE = BASE_DIR / "public_link.txt"

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

server = ThreadingHTTPServer(("127.0.0.1", PORT), QuietHandler)
threading.Thread(target=server.serve_forever, daemon=True).start()

tunnel = ngrok.connect(PORT, "http")
public_url = tunnel.public_url.rstrip("/") + "/tracker.html"
LINK_FILE.write_text(public_url, encoding="utf-8")
print(public_url, flush=True)

try:
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    pass
finally:
    ngrok.kill()
    server.shutdown()
    server.server_close()
