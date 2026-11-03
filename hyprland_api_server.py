#!/usr/bin/env python3
"""
Hyprland Autonomous Local API Server & Cockpit Bridge
====================================================
Zero-dependency HTTP REST & Static Server serving the Hyprland Mission Control Cockpit
and exposing real-time endpoints for Monitors, Workspaces, Clients, Decorations,
Bezier Animations, Window Rules, Socket2 Events, and the 12-Phase Sovereign Lifecycle.

Default Port: 8785
Usage:
    python hyprland_api_server.py [--port 8785]
"""

from __future__ import annotations

import os
import sys
import json
import argparse
import socket
from typing import Any, Dict
from dataclasses import asdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from hyprland_orchestrator import HyprlandClient, HyprlandConfig, HyprlandOrchestrator

client: HyprlandClient = None
orchestrator: HyprlandOrchestrator = None


class HyprlandApiHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for Hyprland REST API and static Cockpit."""

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-API-Key")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def _json_response(self, data: Any, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        body = json.dumps(data, indent=2, default=str).encode("utf-8")
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
        query = parse_qs(parsed.query)

        # Cockpit UI routing
        if path in ("/", "/cockpit", "/hyprland_control_cockpit.html"):
            cockpit_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "hyprland_control_cockpit.html"))
            if os.path.exists(cockpit_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                with open(cockpit_path, "rb") as f:
                    content = f.read()
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                self.send_error(404, "Cockpit HTML template not found")
                return

        # API Endpoints
        if path == "/api/v1/health":
            return self._json_response({
                "status": "healthy",
                "mode": "mock_simulation" if not client.is_live else "live_socket",
                "is_live": client.is_live,
                "timestamp": client.get_info().uptime_seconds
            })

        elif path == "/api/v1/info":
            info = client.get_info()
            return self._json_response(asdict(info))

        elif path == "/api/v1/monitors":
            monitors = client.get_monitors()
            return self._json_response([asdict(m) for m in monitors])

        elif path == "/api/v1/workspaces":
            workspaces = client.get_workspaces()
            return self._json_response([asdict(w) for w in workspaces])

        elif path == "/api/v1/clients":
            clients = client.get_clients()
            return self._json_response([asdict(c) for c in clients])

        elif path == "/api/v1/active-window":
            active = client.get_active_window()
            return self._json_response(asdict(active) if active else None)

        elif path == "/api/v1/decorations":
            return self._json_response(asdict(client.state_store.decorations))

        elif path == "/api/v1/animations":
            return self._json_response({
                "beziers": [asdict(b) for b in client.state_store.beziers.values()],
                "rules": [asdict(r) for r in client.state_store.animation_rules.values()]
            })

        elif path == "/api/v1/rules":
            rules = client.state_store.window_rules
            return self._json_response([asdict(r) for r in rules])

        elif path == "/api/v1/devices":
            devices = client.state_store.input_devices
            return self._json_response([asdict(d) for d in devices])

        elif path == "/api/v1/events":
            since_id = int(query.get("since", ["0"])[0])
            events = client.get_events(since_id=since_id)
            return self._json_response(events)

        elif path == "/api/v1/configs":
            configs = client.generate_modular_config()
            return self._json_response(configs)

        elif path == "/api/v1/manifest":
            if os.path.exists(client.config.manifest_path):
                with open(client.config.manifest_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return self._json_response(data)
            return self._json_response({"error": "Manifest not found. Run /api/v1/do-everything first."}, status=404)

        # Fallback to SimpleHTTPRequestHandler for static files
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._read_body_json()

        if path == "/api/v1/dispatch":
            action = body.get("action", "")
            argument = body.get("argument", "")
            if not action:
                return self._json_response({"error": "Missing 'action' parameter"}, status=400)
            res = client.dispatch(action, argument)
            return self._json_response(res)

        elif path == "/api/v1/keyword":
            key = body.get("key", "")
            val = body.get("value", "")
            if not key or val is None:
                return self._json_response({"error": "Missing 'key' or 'value'"}, status=400)
            res = client.set_keyword(key, str(val))
            return self._json_response(res)

        elif path == "/api/v1/decorations":
            decs = client.set_decorations(**body)
            return self._json_response(asdict(decs))

        elif path == "/api/v1/animations":
            name = body.get("name", "windows")
            enabled = body.get("enabled", True)
            speed = int(body.get("speed", 7))
            curve = body.get("curve", "default")
            style = body.get("style", "")
            rule = client.set_animation(name, enabled=enabled, speed=speed, curve=curve, style=style)
            return self._json_response(asdict(rule))

        elif path == "/api/v1/rules":
            rule_type = body.get("rule_type", "")
            pattern = body.get("pattern", "")
            if not rule_type or not pattern:
                return self._json_response({"error": "Missing 'rule_type' or 'pattern'"}, status=400)
            rule = client.add_window_rule(rule_type, pattern)
            return self._json_response(asdict(rule))

        elif path == "/api/v1/do-everything":
            manifest = orchestrator.do_everything()
            return self._json_response(manifest)

        return self._json_response({"error": f"Endpoint not found: {path}"}, status=404)


def is_port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def find_free_port(preferred: int = 8785, max_attempts: int = 10) -> int:
    for p in range(preferred, preferred + max_attempts):
        if is_port_free(p):
            return p
    return preferred


def run_server(port: int = 8785):
    global client, orchestrator
    client = HyprlandClient()
    orchestrator = HyprlandOrchestrator(client)

    chosen_port = find_free_port(port)
    server_address = ("127.0.0.1", chosen_port)
    httpd = HTTPServer(server_address, HyprlandApiHandler)

    print("=" * 70)
    print("  HYPRLAND AUTONOMOUS API SERVER & COCKPIT BRIDGE")
    print("=" * 70)
    print(f"  Local Endpoint:   http://localhost:{chosen_port}")
    print(f"  Mission Cockpit:  http://localhost:{chosen_port}/cockpit")
    print(f"  API Documentation: http://localhost:{chosen_port}/api/v1/info")
    print(f"  Lifecycle Runner: http://localhost:{chosen_port}/api/v1/do-everything")
    print("=" * 70)
    print("  Press Ctrl+C to stop server.\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Hyprland API Server...")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hyprland Autonomous Local API Server")
    parser.add_argument("--port", type=int, default=8785, help="HTTP Server Port (default: 8785)")
    args = parser.parse_args()
    run_server(args.port)
