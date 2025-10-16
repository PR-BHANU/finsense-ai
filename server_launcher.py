import os
import threading
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", 5005))

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK - FinSense is alive!")

def run_health_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    print(f"✅ Health check running on port {PORT}")
    server.serve_forever()

def run_rasa():
    print("🚀 Starting Rasa server...")
    subprocess.run(["rasa", "run", "--enable-api", "--cors", "*", "--port", str(PORT)])

def run_actions():
    print("🧠 Starting action server...")
    subprocess.run(["rasa", "run", "actions", "--port", "5055"])

if __name__ == "__main__":
    # Start Rasa and Actions concurrently
    threading.Thread(target=run_actions, daemon=True).start()
    threading.Thread(target=run_rasa, daemon=True).start()
    run_health_server()
