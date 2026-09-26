"""
HTTP Server for REVENUE OS Command Center
Adheres strictly to Directives 85, 160.
Serves the 24/7 web command center and handles approval actions.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse, parse_qs
from REVENUE_OS.command_center.cli import RevenueOSCLI
from REVENUE_OS.founder_os.approval_center import ApprovalCenter
from REVENUE_OS.automations.automations import AutomationEngine

WEB_DIR = Path(__file__).resolve().parent.parent / "web"

class RevenueOSRequestHandler(BaseHTTPRequestHandler):
    cli = RevenueOSCLI()
    approval_center = ApprovalCenter()
    automations = AutomationEngine()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/state":
            state = self.cli.get_dashboard_state()
            self._send_json(state)
        elif path == "/api/brief":
            brief = self.cli.get_executive_brief()
            self._send_json({"brief": brief})
        elif path == "/" or path == "/index.html":
            self._serve_file(WEB_DIR / "index.html", "text/html")
        elif path == "/styles.css":
            self._serve_file(WEB_DIR / "styles.css", "text/css")
        elif path == "/app.js":
            self._serve_file(WEB_DIR / "app.js", "application/javascript")
        elif path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if path == "/api/approve":
            req_id = payload.get("id")
            notes = payload.get("notes", "Approved via Command Center Web UI")
            if req_id is not None:
                self.approval_center.approve_request(int(req_id), notes=notes)
                self._send_json({"status": "SUCCESS", "message": f"Request {req_id} APPROVED."})
            else:
                self.send_error(400, "Missing request id")
        elif path == "/api/reject":
            req_id = payload.get("id")
            notes = payload.get("notes", "Rejected via Command Center Web UI")
            if req_id is not None:
                self.approval_center.reject_request(int(req_id), notes=notes)
                self._send_json({"status": "SUCCESS", "message": f"Request {req_id} REJECTED."})
            else:
                self.send_error(400, "Missing request id")
        elif path == "/api/run-automation":
            name = payload.get("name")
            if name:
                res = self.automations.run_automation(name)
                self._send_json(res)
            else:
                self.send_error(400, "Missing automation name")
        else:
            self.send_error(404, "Not Found")

    def _send_json(self, data: dict, status: int = 200):
        encoded = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(encoded)

    def _serve_file(self, file_path: Path, content_type: str):
        if not file_path.exists():
            self.send_error(404, f"File {file_path.name} not found")
            return
        content = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

def create_http_server(host: str = "127.0.0.1", port: int = 8765) -> HTTPServer:
    return HTTPServer((host, port), RevenueOSRequestHandler)

if __name__ == "__main__":
    server = create_http_server()
    print(f"REVENUE OS 24/7 Command Center live at: http://127.0.0.1:8765")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping server.")
        server.server_close()
