#!/usr/bin/env python3
"""
n8n Autonomous Local API Server & Mission Control Bridge
========================================================
Zero-dependency HTTP REST & Static Server serving the n8n Mission Control Cockpit
and exposing real-time endpoints for nodes, workflows, executions, webhooks, and AI agent.

Port: 8771 (Default)
Usage:
    python n8n_api_server.py [--port 8771]
"""

import os
import sys
import json
import argparse
from typing import Any
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from n8n_orchestrator import N8nClient, N8nOrchestrator

BASE_DIR = Path(__file__).parent.resolve()
COCKPIT_HTML = BASE_DIR / "n8n_control_cockpit.html"

client = N8nClient()
orchestrator = N8nOrchestrator(client)


class N8nApiHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for n8n REST API and static Cockpit."""

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-N8N-API-KEY")
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

    def _read_body_json(self) -> dict:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            raw = self.rfile.read(content_length).decode("utf-8")
            try:
                return json.loads(raw)
            except Exception:
                return {"raw": raw}
        return {}

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        # Serve Cockpit UI
        if path in ("/", "/cockpit", "/cockpit.html"):
            if COCKPIT_HTML.exists():
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                content = COCKPIT_HTML.read_bytes()
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                self.send_error(404, "Cockpit HTML file not found.")
                return

        # API Endpoints
        if path == "/api/health":
            self._json_response(client.get_health())
        elif path == "/api/telemetry":
            self._json_response(client.get_telemetry())
        elif path == "/api/nodes":
            grp = qs.get("group", [None])[0]
            limit = int(qs.get("limit", [50])[0])
            self._json_response(client.list_nodes(group=grp, limit=limit))
        elif path == "/api/nodes/search":
            q = qs.get("q", [""])[0]
            limit = int(qs.get("limit", [15])[0])
            self._json_response(client.search_nodes(query=q, limit=limit))
        elif path == "/api/workflows":
            active_only = qs.get("active", ["false"])[0].lower() in ("true", "1")
            self._json_response(client.list_workflows(active_only=active_only))
        elif path.startswith("/api/workflows/"):
            wf_id = path[len("/api/workflows/"):].strip("/")
            wf = client.get_workflow(wf_id)
            if wf:
                self._json_response(wf)
            else:
                self._json_response({"error": "Workflow not found"}, status=404)
        elif path == "/api/executions":
            limit = int(qs.get("limit", [20])[0])
            status = qs.get("status", [None])[0]
            self._json_response(client.list_executions(status=status, limit=limit))
        elif path.startswith("/api/executions/"):
            exec_id = path[len("/api/executions/"):].strip("/")
            e = client.get_execution(exec_id)
            if e:
                self._json_response(e)
            else:
                self._json_response({"error": "Execution not found"}, status=404)
        elif path == "/api/credentials":
            self._json_response(client.list_credentials())
        elif path == "/api/dropzone":
            self._json_response(client.scan_dropzone())
        else:
            self.send_error(404, f"Path not found: {path}")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._read_body_json()

        if path.startswith("/api/workflows/") and path.endswith("/run"):
            wf_id = path[len("/api/workflows/"): -len("/run")].strip("/")
            try:
                res = client.execute_workflow(wf_id, input_data=body)
                self._json_response(res)
            except Exception as e:
                self._json_response({"error": str(e)}, status=400)
        elif path.startswith("/webhook/"):
            webhook_path = path[len("/webhook/"):].strip("/")
            res = client.trigger_webhook(webhook_path, body, test_mode=False)
            self._json_response(res)
        elif path.startswith("/webhook-test/"):
            webhook_path = path[len("/webhook-test/"):].strip("/")
            res = client.trigger_webhook(webhook_path, body, test_mode=True)
            self._json_response(res)
        elif path == "/api/ai/agent":
            prompt = body.get("prompt", "Analyze system health")
            context = body.get("context")
            res = client.run_ai_agent(prompt, context=context)
            self._json_response(res)
        elif path == "/api/lifecycle/do-everything":
            res = orchestrator.do_everything()
            self._json_response(res)
        elif path == "/api/dropzone/scan":
            self._json_response(client.scan_dropzone())
        else:
            self.send_error(404, f"Post route not found: {path}")


def run_server(port: int = 8771):
    server_address = ("", port)
    httpd = HTTPServer(server_address, N8nApiHandler)
    print(f"\n[+] n8n Autonomous API Server & Cockpit live at http://localhost:{port}")
    print(f"    - Mission Control Cockpit: http://localhost:{port}/cockpit")
    print(f"    - Health Check:            http://localhost:{port}/api/health")
    print(f"    - Node FTS5 Search:        http://localhost:{port}/api/nodes/search?q=webhook")
    print(f"    - Webhook Dispatcher:      http://localhost:{port}/webhook/<path>\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down n8n API server.")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="n8n Local API Server")
    parser.add_argument("--port", type=int, default=8771, help="Port to bind (default 8771)")
    args = parser.parse_args()
    run_server(args.port)
