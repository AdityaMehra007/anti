"""
FORTUNE 500 HIGH-CONCURRENCY REST API SERVER
============================================
Lightweight, zero-dependency multi-threaded HTTP/REST daemon serving
the Fortune 500 Project Catalog, Live Execution Engine, and Telemetry API.

Governed by OMEGA Constitution & Ponytail Minimalist Architecture.
"""

import os
import sys
import json
import time
import urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, List

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
COCKPIT_HTML_PATH = os.path.join(BASE_DIR, "fortune_500_cockpit.html")
MASTER_JSON_PATH = os.path.join(DATA_DIR, "fortune_500_projects_master.json")
TELEMETRY_JSON_PATH = os.path.join(DATA_DIR, "fortune_500_execution_telemetry.json")

# Lazy-loaded cache
_PROJECTS_CACHE: List[Dict[str, Any]] = []
_SERVER_START_TIME = time.time()


def get_projects() -> List[Dict[str, Any]]:
    global _PROJECTS_CACHE
    if not _PROJECTS_CACHE:
        if os.path.exists(MASTER_JSON_PATH):
            with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                _PROJECTS_CACHE = data.get("projects", [])
    return _PROJECTS_CACHE


class Fortune500RequestHandler(BaseHTTPRequestHandler):
    server_version = "Fortune500Engine/1.0"

    def _send_json(self, status: int, data: Any):
        payload = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(payload)

    def _send_html(self, status: int, html_content: str):
        payload = html_content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')
        query = urllib.parse.parse_qs(parsed.query)

        # 1. Root: Serves the Cockpit UI
        if path == "" or path == "/cockpit":
            if os.path.exists(COCKPIT_HTML_PATH):
                with open(COCKPIT_HTML_PATH, "r", encoding="utf-8") as f:
                    self._send_html(200, f.read())
            else:
                self._send_html(404, "<h1>Cockpit file not found</h1>")
            return

        # 2. Health check
        if path == "/health":
            projects = get_projects()
            self._send_json(200, {
                "status": "ONLINE",
                "uptime_seconds": round(time.time() - _SERVER_START_TIME, 2),
                "total_projects": len(projects),
                "governance": "OMEGA_CONSTITUTION_120_DIRECTIVES",
                "engine": "Fortune 500 Sovereign Execution Daemon"
            })
            return

        # 3. Telemetry & Benchmarks
        if path == "/api/telemetry" or path == "/api/benchmarks":
            if os.path.exists(TELEMETRY_JSON_PATH):
                with open(TELEMETRY_JSON_PATH, "r", encoding="utf-8") as f:
                    self._send_json(200, json.load(f))
            else:
                self._send_json(200, {"message": "Telemetry initializing", "status": "PENDING"})
            return

        # 4. Filterable Projects API
        if path == "/api/projects":
            projects = get_projects()
            q = query.get("q", [""])[0].lower().strip()
            sector = query.get("sector", [""])[0].lower().strip()
            tier = query.get("tier", [""])[0].upper().strip()

            filtered = projects
            if q:
                filtered = [
                    p for p in filtered
                    if q in p["company"].lower()
                    or q in p["ticker"].lower()
                    or q in p["project_codename"].lower()
                    or q in p["tech_stack"].lower()
                ]
            if sector and sector != "all":
                filtered = [p for p in filtered if sector in p["sector"].lower()]
            if tier:
                if tier == "TOP50":
                    filtered = [p for p in filtered if p["rank"] <= 50]
                elif tier == "TOP100":
                    filtered = [p for p in filtered if p["rank"] <= 100]
                elif tier == "MID250":
                    filtered = [p for p in filtered if 101 <= p["rank"] <= 250]
                elif tier == "NEXT250":
                    filtered = [p for p in filtered if 251 <= p["rank"] <= 500]

            # Pagination
            page = int(query.get("page", [1])[0])
            limit = int(query.get("limit", [50])[0])
            start_idx = (page - 1) * limit
            end_idx = start_idx + limit
            paged = filtered[start_idx:end_idx]

            self._send_json(200, {
                "total_matched": len(filtered),
                "page": page,
                "limit": limit,
                "total_pages": max(1, (len(filtered) + limit - 1) // limit),
                "projects": paged
            })
            return

        # 5. Single Project by Rank: /api/projects/<rank>
        if path.startswith("/api/projects/"):
            parts = path.split("/")
            if len(parts) == 4 and parts[3].isdigit():
                rank = int(parts[3])
                projects = get_projects()
                match = next((p for p in projects if p["rank"] == rank), None)
                if match:
                    self._send_json(200, match)
                else:
                    self._send_json(404, {"error": f"Project with rank #{rank} not found."})
                return

        # Fallback 404
        self._send_json(404, {"error": "Endpoint not found", "path": path})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')

        # Execute Project: POST /api/execute/<rank>
        if path.startswith("/api/execute/"):
            parts = path.split("/")
            if len(parts) == 4 and parts[3].isdigit():
                rank = int(parts[3])
                projects = get_projects()
                target_proj = next((p for p in projects if p["rank"] == rank), None)
                if not target_proj:
                    self._send_json(404, {"error": f"Enterprise with rank #{rank} not found"})
                    return

                # Import and execute via Swarm Orchestrator
                from fortune_500_swarm_orchestrator import execute_single_project
                result = execute_single_project(target_proj)
                self._send_json(200, result)
                return

        # Batch Execute: POST /api/execute-batch
        if path == "/api/execute-batch":
            from fortune_500_swarm_orchestrator import run_swarm_batch
            # Read optional limit from body
            length = int(self.headers.get("Content-Length", 0))
            limit = 50
            if length > 0:
                try:
                    body = json.loads(self.wfile.read(length).decode("utf-8"))
                    limit = body.get("limit", 50)
                except Exception:
                    pass
            report = run_swarm_batch(max_workers=8, limit=limit)
            self._send_json(200, report["metadata"])
            return

        self._send_json(404, {"error": "POST Endpoint not found", "path": path})

    def log_message(self, format, *args):
        # Override to suppress noisy stdout during high-speed traffic
        if "404" in args or "500" in args:
            sys.stderr.write(f"[{time.strftime('%X')}] {format % args}\n")


def run_server(port: int = 8888, host: str = "127.0.0.1"):
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, Fortune500RequestHandler)
    print(f"[+] Fortune 500 REST API Server active at http://{host}:{port}/")
    print(f"    - Cockpit UI: http://{host}:{port}/cockpit")
    print(f"    - Health:     http://{host}:{port}/health")
    print(f"    - Projects:   http://{host}:{port}/api/projects")
    print(f"    - Telemetry:  http://{host}:{port}/api/telemetry")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down server gracefully...")
        httpd.shutdown()


if __name__ == "__main__":
    port = 8888
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port=port)
