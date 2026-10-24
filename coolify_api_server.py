#!/usr/bin/env python3
"""
Coolify Autonomous Local API Server & Cockpit Bridge
===================================================
Zero-dependency HTTP REST & Static Server serving the Coolify Mission Control Cockpit
and exposing real-time endpoints for servers, apps, databases, deployments, and templates.

Port: 8767 (Default)
Usage:
    python coolify_api_server.py [--port 8767]
"""

import os
import sys
import json
import argparse
from typing import Any
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from coolify_orchestrator import CoolifyClient, CoolifyOrchestrator, CoolifyTemplateCatalog
from coolify_compose_exporter import CoolifyComposeExporter

client = CoolifyClient()
orchestrator = CoolifyOrchestrator(client)
catalog = CoolifyTemplateCatalog()
exporter = CoolifyComposeExporter()


class CoolifyApiHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for Coolify REST API and static Cockpit."""

    def end_headers(self):
        # Enable CORS for local cross-origin cockpit interaction
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

        # Root route redirects to Cockpit
        if path == "/" or path == "":
            self.path = "/coolify_control_cockpit.html"
            return super().do_GET()

        # API Endpoints
        if path == "/api/status":
            return self._json_response(orchestrator.get_cluster_status())
        elif path == "/api/servers":
            return self._json_response(client.list_servers())
        elif path == "/api/apps":
            return self._json_response(client.list_applications())
        elif path == "/api/dbs":
            return self._json_response(client.list_databases())
        elif path == "/api/services":
            return self._json_response(client.list_services())
        elif path == "/api/catalog":
            q = params.get("search", [""])[0]
            cat = params.get("category", [""])[0]
            return self._json_response(catalog.search(query=q, category=cat))
        elif path.startswith("/api/templates/"):
            tpl_id = path.replace("/api/templates/", "").strip("/")
            tpl = catalog.get_template(tpl_id)
            if tpl:
                return self._json_response(tpl)
            return self._json_response({"error": "Template not found"}, status=404)

        # Fallback to static file server
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if path == "/api/deploy":
            res_uuid = payload.get("uuid", "app-omega-api")
            force = payload.get("force_rebuild", False)
            res = client.deploy(res_uuid, force_rebuild=force)
            return self._json_response(res)
        elif path == "/api/stack":
            res = orchestrator.provision_full_omega_stack()
            return self._json_response(res)
        elif path == "/api/compose":
            tpl_id = payload.get("template", "anythingllm")
            domain = payload.get("domain", "localhost")
            try:
                compose_yml, env_vars = exporter.export(tpl_id, domain=domain)
                return self._json_response({"compose": compose_yml, "env": env_vars})
            except Exception as e:
                return self._json_response({"error": str(e)}, status=400)

        return self._json_response({"error": f"Endpoint not found: {path}"}, status=404)


def run_server(port: int = 8767):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, CoolifyApiHandler)
    print(f"[*] Coolify Autonomous API & Cockpit Server online at http://127.0.0.1:{port}/")
    print(f"[*] Direct Cockpit URL: http://127.0.0.1:{port}/coolify_control_cockpit.html")
    print("Press Ctrl+C to terminate.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down Coolify API server.")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coolify Autonomous API Server")
    parser.add_argument("--port", type=int, default=8767, help="Server port (default: 8767)")
    args = parser.parse_args()
    run_server(args.port)
