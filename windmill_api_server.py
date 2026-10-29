#!/usr/bin/env python3
"""
Windmill Autonomous Local API Server & Cockpit Bridge
=====================================================
Zero-dependency HTTP REST & Static Server serving the Windmill Mission Control Cockpit
and exposing real-time endpoints for scripts, flows/DAGs, jobs, resources, and Hub templates.

Port: 8768 (Default)
Usage:
    python windmill_api_server.py [--port 8768]
"""

import os
import sys
import json
import argparse
from typing import Any
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from windmill_orchestrator import WindmillClient, WindmillOrchestrator

client = WindmillClient()
orchestrator = WindmillOrchestrator(client)


class WindmillApiHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for Windmill REST API and static Cockpit."""

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

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        # Root redirects to Windmill Control Cockpit
        if path == "/" or path == "":
            self.path = "/windmill_control_cockpit.html"
            return super().do_GET()

        # Static assets
        if path.endswith(".html") or path.endswith(".css") or path.endswith(".js") or path.endswith(".json"):
            if os.path.exists(os.path.join(os.getcwd(), path.lstrip("/"))):
                return super().do_GET()

        # REST API endpoints
        if path == "/health":
            return self._json_response({"status": "ok", "service": "windmill_bridge"})
        elif path == "/api/info" or path == "/api/status":
            return self._json_response(client.get_telemetry())
        elif path == "/api/workspaces":
            return self._json_response(client.list_workspaces())
        elif path == "/api/scripts":
            return self._json_response(client.list_scripts())
        elif path.startswith("/api/scripts/"):
            script_path = path.replace("/api/scripts/", "").strip("/")
            s = client.get_script(script_path)
            if s:
                return self._json_response(s)
            return self._json_response({"error": "Script not found"}, status=404)
        elif path == "/api/flows":
            return self._json_response(client.list_flows())
        elif path.startswith("/api/flows/"):
            flow_path = path.replace("/api/flows/", "").strip("/")
            f = client.get_flow(flow_path)
            if f:
                return self._json_response(f)
            return self._json_response({"error": "Flow not found"}, status=404)
        elif path == "/api/jobs":
            limit = int(params.get("limit", [50])[0])
            st = params.get("status", [None])[0]
            return self._json_response(client.list_jobs(limit=limit, status=st))
        elif path.startswith("/api/jobs/"):
            job_id = path.replace("/api/jobs/", "").strip("/")
            j = client.get_job(job_id)
            if j:
                return self._json_response(j)
            return self._json_response({"error": "Job not found"}, status=404)
        elif path == "/api/resources":
            return self._json_response(client.list_resources())
        elif path == "/api/apps":
            return self._json_response(client.list_apps())
        elif path == "/api/schedules":
            return self._json_response(client.list_schedules())
        elif path == "/api/variables":
            return self._json_response(client.list_variables())
        elif path == "/api/hub":
            q = params.get("search", [""])[0]
            cat = params.get("category", [""])[0]
            return self._json_response(client.search_hub(query=q, category=cat))
        elif path == "/api/overview":
            return self._json_response(orchestrator.get_platform_overview())

        # Fallback to static handler
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            data = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            data = {}

        if path == "/api/scripts/run":
            script_path = data.get("path", "")
            args = data.get("args", {})
            if not script_path:
                return self._json_response({"error": "Missing 'path' parameter"}, status=400)
            res = client.run_script(script_path, args)
            return self._json_response(res)

        elif path == "/api/flows/run":
            flow_path = data.get("path", "")
            args = data.get("args", {})
            if not flow_path:
                return self._json_response({"error": "Missing 'path' parameter"}, status=400)
            res = client.execute_flow(flow_path, args)
            return self._json_response(res)

        elif path == "/api/jobs/approve":
            job_id = data.get("job_id", "")
            approved = data.get("approved", True)
            notes = data.get("notes", "")
            if not job_id:
                return self._json_response({"error": "Missing 'job_id' parameter"}, status=400)
            res = client.approve_job(job_id, approved=approved, notes=notes)
            return self._json_response(res)

        elif path == "/api/resources":
            res_path = data.get("path", "")
            res_type = data.get("resource_type", "custom")
            val = data.get("value", {})
            desc = data.get("description", "")
            if not res_path:
                return self._json_response({"error": "Missing 'path' parameter"}, status=400)
            res = client.create_resource(res_path, res_type, val, desc)
            return self._json_response(res, status=201)

        elif path == "/api/hub/import":
            hub_id = data.get("hub_id", "")
            if not hub_id:
                return self._json_response({"error": "Missing 'hub_id' parameter"}, status=400)
            res = client.import_from_hub(hub_id)
            return self._json_response(res)

        elif path == "/api/schedules/trigger":
            sched_path = data.get("path", "")
            if not sched_path:
                return self._json_response({"error": "Missing 'path' parameter"}, status=400)
            res = client.trigger_schedule(sched_path)
            return self._json_response(res)

        elif path == "/api/variables/set":
            var_path = data.get("path", "")
            val = data.get("value")
            sec = data.get("is_secret", False)
            desc = data.get("description", "")
            if not var_path:
                return self._json_response({"error": "Missing 'path' parameter"}, status=400)
            res = client.set_variable(var_path, val, is_secret=sec, description=desc)
            return self._json_response(res)

        elif path.startswith("/api/webhooks/"):
            hook_name = path.replace("/api/webhooks/", "").strip("/")
            res = client.trigger_webhook(hook_name, data)
            return self._json_response(res)

        elif path == "/api/do-everything":
            manifest = orchestrator.do_everything()
            return self._json_response(manifest)

        return self._json_response({"error": f"Endpoint not found: {path}"}, status=404)


def run_server(port: int = 8768):
    server_address = ("127.0.0.1", port)
    try:
        httpd = HTTPServer(server_address, WindmillApiHandler)
        print(f"[*] Windmill Autonomous API Server running at: http://localhost:{port}/")
        print(f"[*] Serving Windmill Control Cockpit at:     http://localhost:{port}/windmill_control_cockpit.html")
        httpd.serve_forever()
    except OSError as e:
        if port < 8780:
            print(f"[!] Port {port} occupied, attempting port {port + 1}...")
            run_server(port + 1)
        else:
            print(f"[ERROR] Failed to bind server: {e}")
            sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Windmill Local API Bridge Server")
    parser.add_argument("--port", type=int, default=8768, help="Port to bind (default: 8768)")
    args = parser.parse_args()
    run_server(args.port)
