#!/usr/bin/env python3
"""
Plane Autonomous Local API Server & Cockpit Bridge
=================================================
Zero-dependency HTTP REST & Static Server serving the Plane Mission Control Cockpit
and exposing real-time endpoints for Workspaces, Projects, Issues, Cycles,
Modules, Pages, Triage, Analytics, and the 12-Phase Sovereign Lifecycle.

Default Port: 8774
Usage:
    python plane_api_server.py [--port 8774]
"""

import os
import sys
import json
import argparse
import socket
from typing import Any, Dict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from plane_orchestrator import PlaneConfig, PlaneOrchestrator

orchestrator: PlaneOrchestrator = None


class PlaneApiHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for Plane REST API and static Cockpit."""

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
            cockpit_file = os.path.join(os.path.dirname(__file__), "plane_control_cockpit.html")
            if os.path.exists(cockpit_file):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                with open(cockpit_file, "rb") as f:
                    content = f.read()
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                self._json_response({"error": "plane_control_cockpit.html not found"}, 404)
                return

        # API Endpoints
        if path == "/api/health":
            self._json_response({"status": "healthy", "service": "plane_api_bridge", "mode": orchestrator.get_info()["mode"]})
            return

        if path == "/api/info":
            self._json_response(orchestrator.get_info())
            return

        if path == "/api/workspaces":
            self._json_response(orchestrator.list_workspaces())
            return

        if path == "/api/projects":
            ws = params.get("workspace", [None])[0]
            self._json_response(orchestrator.list_projects(ws))
            return

        if path == "/api/states":
            pid = params.get("project_id", ["proj-core-01"])[0]
            self._json_response(orchestrator.list_states(pid))
            return

        if path == "/api/issues":
            pid = params.get("project_id", [None])[0]
            cid = params.get("cycle_id", [None])[0]
            group = params.get("state_group", [None])[0]
            self._json_response(orchestrator.list_issues(project_id=pid, cycle_id=cid, state_group=group))
            return

        if path == "/api/cycles":
            pid = params.get("project_id", [None])[0]
            self._json_response(orchestrator.list_cycles(project_id=pid))
            return

        if path.startswith("/api/cycles/") and path.endswith("/burndown"):
            # /api/cycles/{id}/burndown
            parts = path.strip("/").split("/")
            cid = parts[2]
            self._json_response(orchestrator.get_burndown(cid))
            return

        if path == "/api/modules":
            pid = params.get("project_id", [None])[0]
            self._json_response(orchestrator.list_modules(project_id=pid))
            return

        if path == "/api/pages":
            pid = params.get("project_id", [None])[0]
            self._json_response(orchestrator.list_pages(project_id=pid))
            return

        if path == "/api/views":
            pid = params.get("project_id", [None])[0]
            self._json_response(orchestrator.list_views(project_id=pid))
            return

        if path == "/api/triage":
            pid = params.get("project_id", [None])[0]
            self._json_response(orchestrator.list_triage(project_id=pid))
            return

        if path == "/api/analytics":
            pid = params.get("project_id", [None])[0]
            self._json_response(orchestrator.get_analytics(project_id=pid))
            return

        if path == "/api/docker-config":
            self._json_response(orchestrator.generate_docker_compose_config())
            return

        # Fallback to base static handler if requested file exists
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._read_body_json()

        if path == "/api/projects":
            name = body.get("name")
            ident = body.get("identifier")
            if not name or not ident:
                self._json_response({"error": "name and identifier required"}, 400)
                return
            res = orchestrator.create_project(
                name=name,
                identifier=ident,
                description=body.get("description", ""),
                emoji=body.get("emoji", "⚡"),
                workspace_slug=body.get("workspace_slug")
            )
            self._json_response(res, 201)
            return

        if path == "/api/issues":
            name = body.get("name")
            pid = body.get("project_id", "proj-core-01")
            if not name:
                self._json_response({"error": "name required"}, 400)
                return
            res = orchestrator.create_issue(
                name=name,
                project_id=pid,
                description_html=body.get("description_html", ""),
                priority=body.get("priority", "medium"),
                estimate_point=body.get("estimate_point"),
                cycle_id=body.get("cycle_id"),
                module_id=body.get("module_id")
            )
            self._json_response(res, 201)
            return

        if path.startswith("/api/issues/") and path.endswith("/update"):
            parts = path.strip("/").split("/")
            iss_id = parts[2]
            res = orchestrator.update_issue(iss_id, body)
            if res:
                self._json_response(res)
            else:
                self._json_response({"error": "issue not found"}, 404)
            return

        if path == "/api/cycles":
            name = body.get("name")
            pid = body.get("project_id", "proj-core-01")
            start_date = body.get("start_date")
            end_date = body.get("end_date")
            if not name or not start_date or not end_date:
                self._json_response({"error": "name, start_date, and end_date required"}, 400)
                return
            res = orchestrator.create_cycle(
                name=name,
                project_id=pid,
                start_date=start_date,
                end_date=end_date,
                description=body.get("description", "")
            )
            self._json_response(res, 201)
            return

        if path == "/api/modules":
            name = body.get("name")
            pid = body.get("project_id", "proj-core-01")
            if not name:
                self._json_response({"error": "name required"}, 400)
                return
            res = orchestrator.create_module(
                name=name,
                project_id=pid,
                description=body.get("description", ""),
                lead_id=body.get("lead_id", "omega-prime"),
                target_date=body.get("target_date")
            )
            self._json_response(res, 201)
            return

        if path == "/api/pages":
            title = body.get("title")
            desc = body.get("description_html", "")
            pid = body.get("project_id", "proj-core-01")
            if not title:
                self._json_response({"error": "title required"}, 400)
                return
            res = orchestrator.create_page(
                title=title,
                description_html=desc,
                project_id=pid,
                summary_ai=body.get("summary_ai", "")
            )
            self._json_response(res, 201)
            return

        if path.startswith("/api/triage/") and path.endswith("/action"):
            parts = path.strip("/").split("/")
            t_id = parts[2]
            act = body.get("action", "accept")
            res = orchestrator.triage_action(t_id, act)
            self._json_response(res)
            return

        if path == "/api/do-everything":
            res = orchestrator.do_everything()
            self._json_response(res)
            return

        self._json_response({"error": f"Path not found: {path}"}, 404)


def find_free_port(preferred: int = 8774, max_attempts: int = 12) -> int:
    """Attempt to bind preferred port; otherwise increment up to max_attempts."""
    for p in range(preferred, preferred + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", p)) != 0:
                return p
    return preferred


def run_server(port: int = 8774):
    global orchestrator
    orchestrator = PlaneOrchestrator()
    chosen_port = find_free_port(port)

    server_address = ("127.0.0.1", chosen_port)
    httpd = HTTPServer(server_address, PlaneApiHandler)

    print("===============================================================================")
    print("      PLANE AUTONOMOUS MISSION CONTROL API SERVER & COCKPIT BRIDGE             ")
    print(f"      Listening on: http://127.0.0.1:{chosen_port}                            ")
    print(f"      Mission Cockpit UI: http://127.0.0.1:{chosen_port}/cockpit               ")
    print("===============================================================================")
    sys.stdout.flush()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] Plane API Server shutdown gracefully.")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plane Local API Server & Cockpit Bridge")
    parser.add_argument("--port", type=int, default=8774, help="HTTP Server Port")
    args = parser.parse_args()
    run_server(args.port)
