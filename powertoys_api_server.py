#!/usr/bin/env python3
"""
Microsoft PowerToys Autonomous Local API Server & Cockpit Bridge
================================================================
Zero-dependency HTTP REST & Static Server serving the PowerToys Mission Control Cockpit
and exposing real-time endpoints for FancyZones, PowerToys Run, Awake, Keyboard Manager,
Hosts File Editor, Advanced Paste, Workspaces, and the 12-phase sovereign lifecycle.

Default Port: 8770
Usage:
    python powertoys_api_server.py [--port 8770]
"""

import os
import sys
import json
import argparse
import socket
from typing import Any, Dict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from powertoys_orchestrator import PowerToysConfig, PowerToysOrchestrator

orchestrator: PowerToysOrchestrator = None


class PowerToysApiHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for PowerToys REST API and static Cockpit."""

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def _json_response(self, data: Any, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body_json(self) -> Dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length == 0:
                return {}
            raw = self.rfile.read(length).decode("utf-8")
            return json.loads(raw)
        except Exception:
            return {}

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        # Cockpit static route
        if path in ("/", "/cockpit"):
            cockpit_file = os.path.join(os.path.dirname(__file__), "powertoys_control_cockpit.html")
            if os.path.exists(cockpit_file):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                with open(cockpit_file, "rb") as f:
                    content = f.read()
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        # API Endpoints
        if path == "/api/v1/info":
            self._json_response(orchestrator.get_info())

        elif path == "/api/v1/modules":
            self._json_response(orchestrator.list_modules())

        elif path == "/api/v1/fancyzones/calculate":
            layout_id = params.get("layout", ["priority-grid-01"])[0]
            res_str = params.get("res", ["1920x1080"])[0]
            try:
                w, h = map(int, res_str.lower().split("x"))
            except Exception:
                w, h = (1920, 1080)
            self._json_response(orchestrator.calculate_fancyzones(layout_id, (w, h)))

        elif path == "/api/v1/run":
            query = params.get("q", [""])[0]
            self._json_response(orchestrator.query_pt_run(query))

        elif path == "/api/v1/awake":
            self._json_response(orchestrator.mock_engine.awake)

        elif path == "/api/v1/keyboard/remaps":
            self._json_response(orchestrator.get_keyboard_remaps())

        elif path == "/api/v1/hosts":
            self._json_response(orchestrator.get_hosts())

        elif path == "/api/v1/workspaces":
            self._json_response(orchestrator.mock_engine.workspaces)

        elif path == "/api/v1/security-audit":
            self._json_response(orchestrator.audit_security())

        elif path == "/api/v1/benchmark":
            iterations = int(params.get("iterations", ["1000"])[0])
            self._json_response(orchestrator.benchmark(iterations))

        elif path == "/api/v1/manifest":
            manifest_path = os.path.join("omega", "data", "powertoys_do_everything_manifest.json")
            if os.path.exists(manifest_path):
                with open(manifest_path, "r", encoding="utf-8") as f:
                    self._json_response(json.load(f))
            else:
                self._json_response({"status": "MANIFEST_NOT_FOUND", "message": "Run do-everything first."}, 404)

        else:
            self._json_response({"error": "Endpoint not found", "path": path}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._read_body_json()

        if path == "/api/v1/modules/toggle":
            module_name = body.get("module")
            if not module_name:
                self._json_response({"error": "Missing 'module' parameter"}, 400)
                return
            enabled = body.get("enabled", None)
            res = orchestrator.toggle_module(module_name, enabled)
            self._json_response(res)

        elif path == "/api/v1/awake":
            mode = body.get("mode", "INDEFINITE")
            minutes = body.get("minutes", 60)
            keep_display = body.get("keep_display", True)
            try:
                res = orchestrator.set_awake(mode, minutes, keep_display)
                self._json_response(res)
            except Exception as e:
                self._json_response({"error": str(e)}, 400)

        elif path == "/api/v1/keyboard/remap":
            orig = body.get("original_key")
            new_k = body.get("new_key")
            if not orig or not new_k:
                self._json_response({"error": "Missing 'original_key' or 'new_key'"}, 400)
                return
            res = orchestrator.add_key_remap(orig, new_k)
            self._json_response(res)

        elif path == "/api/v1/hosts":
            ip = body.get("ip")
            host = body.get("host")
            comment = body.get("comment", "")
            if not ip or not host:
                self._json_response({"error": "Missing 'ip' or 'host'"}, 400)
                return
            res = orchestrator.add_hosts(ip, host, comment)
            self._json_response(res)

        elif path == "/api/v1/paste/transform":
            text = body.get("text", "")
            transformation = body.get("transformation", "plain_text")
            prompt = body.get("prompt")
            res = orchestrator.transform_paste(text, transformation, prompt)
            self._json_response(res)

        elif path == "/api/v1/ocr":
            bbox = body.get("bbox", [100, 100, 600, 400])
            res = orchestrator.extract_ocr(tuple(bbox))
            self._json_response(res)

        elif path == "/api/v1/workspaces/launch":
            name = body.get("name", "Full-Stack Dev")
            res = orchestrator.launch_workspace(name)
            self._json_response(res)

        elif path == "/api/v1/do-everything":
            res = orchestrator.do_everything()
            self._json_response(res)

        else:
            self._json_response({"error": "Endpoint not found", "path": path}, 404)


def is_port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def find_free_port(preferred: int = 8770, max_attempts: int = 10) -> int:
    for p in range(preferred, preferred + max_attempts):
        if is_port_free(p):
            return p
    return preferred


def run_server(port: int = 8770):
    global orchestrator
    orchestrator = PowerToysOrchestrator()

    chosen_port = find_free_port(port)
    server_address = ("127.0.0.1", chosen_port)
    httpd = HTTPServer(server_address, PowerToysApiHandler)

    print("=" * 70)
    print("  MICROSOFT POWERTOYS AUTONOMOUS REST API SERVER & COCKPIT")
    print(f"  Local Endpoint:   http://localhost:{chosen_port}")
    print(f"  Mission Cockpit:  http://localhost:{chosen_port}/cockpit")
    print(f"  API Documentation: http://localhost:{chosen_port}/api/v1/info")
    print("=" * 70)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping PowerToys API Server.")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PowerToys Autonomous API Server")
    parser.add_argument("--port", type=int, default=8770, help="HTTP Server Port")
    args = parser.parse_args()
    run_server(args.port)
