from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5005))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"✅ Health server running on port {port}")
    server.serve_forever()
