from http.server import BaseHTTPRequestHandler, HTTPServer
import os, threading, subprocess

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    port = int(os.environ.get("PORT", 5005))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"✅ Health server running on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    # Run Rasa in the background
    threading.Thread(target=lambda: subprocess.run([
        "rasa", "run", "--enable-api", "--cors", "*", "--port", os.environ.get("PORT", "5005")
    ])).start()

    # Start the simple HTTP health endpoint
    run_health_server()
