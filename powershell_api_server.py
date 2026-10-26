#!/usr/bin/env python3
"""
PowerShell Autonomous Local API Server & Cockpit Bridge
=======================================================
Zero-dependency HTTP REST & Static Server serving the PowerShell Mission Control Cockpit
and exposing real-time endpoints for PowerShell scripts, AST parsing, PSScriptAnalyzer,
runbooks, and PSGallery extensions.

Default Port: 8769
Usage:
    python powershell_api_server.py [--port 8769] [--mock]
"""

import os
import sys
import json
import argparse
import socket
from typing import Any
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from powershell_orchestrator import (
    PowerShellConfig,
    PowerShellClient,
    PowerShellOrchestrator
)

client: PowerShellClient = None
orchestrator: PowerShellOrchestrator = None


class PowerShellApiHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for PowerShell REST API and static Cockpit."""

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

        # Root cockpit route
        if path in ("/", "/cockpit"):
            cockpit_file = os.path.join(os.path.dirname(__file__), "powershell_control_cockpit.html")
            if os.path.exists(cockpit_file):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                with open(cockpit_file, "rb") as f:
                    content = f.read()
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        # REST API Routes
        if path == "/api/v1/telemetry":
            return self._json_response(client.get_telemetry())

        elif path == "/api/v1/modules":
            return self._json_response({"modules": client.list_modules()})

        elif path == "/api/v1/gallery":
            qs = parse_qs(parsed.query)
            kw = qs.get("keyword", [""])[0]
            cat = qs.get("category", [""])[0]
            pkgs = client.find_gallery_module(keyword=kw, category=cat)
            return self._json_response({"packages": pkgs})

        elif path == "/api/v1/runbooks":
            return self._json_response({"runbooks": client.list_runbooks()})

        elif path == "/api/v1/runspaces":
            return self._json_response({"runspaces": client.list_runspaces()})

        elif path == "/api/v1/manifest":
            manifest_path = os.path.join("omega", "data", "powershell_do_everything_manifest.json")
            if os.path.exists(manifest_path):
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest_data = json.load(f)
                return self._json_response(manifest_data)
            return self._json_response({"status": "NOT_GENERATED", "message": "Manifest not found. Run /api/v1/do-everything first."}, 404)

        # Fallback to static file serving
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        try:
            payload = json.loads(body) if body else {}
        except Exception as e:
            return self._json_response({"error": f"Invalid JSON payload: {e}"}, 400)

        if path == "/api/v1/exec":
            cmd = payload.get("command", "")
            as_json = payload.get("as_json", True)
            if not cmd:
                return self._json_response({"error": "Missing 'command' parameter"}, 400)
            res = client.execute(cmd, as_json=as_json)
            return self._json_response({
                "stdout": res.stdout,
                "stderr": res.stderr,
                "exit_code": res.exit_code,
                "execution_time_ms": res.execution_time_ms,
                "success": res.success,
                "objects": res.objects
            })

        elif path == "/api/v1/ast":
            code = payload.get("script_content", "")
            if not code:
                return self._json_response({"error": "Missing 'script_content' parameter"}, 400)
            ast_res = client.parse_ast(code)
            return self._json_response({
                "tokens_count": ast_res.tokens_count,
                "functions": ast_res.functions,
                "parameters": ast_res.parameters,
                "pipeline_calls": ast_res.pipeline_calls,
                "variables_referenced": ast_res.variables_referenced,
                "syntax_errors": ast_res.syntax_errors,
                "has_errors": ast_res.has_errors
            })

        elif path == "/api/v1/analyze":
            code = payload.get("script_content", "")
            if not code:
                return self._json_response({"error": "Missing 'script_content' parameter"}, 400)
            diags = client.analyze_script(code)
            return self._json_response({
                "diagnostics": [
                    {
                        "rule_name": d.rule_name,
                        "severity": d.severity,
                        "message": d.message,
                        "line_number": d.line_number,
                        "suggested_fix": d.suggested_fix
                    }
                    for d in diags
                ]
            })

        elif path == "/api/v1/runbooks/run":
            runbook_id = payload.get("runbook_id")
            params = payload.get("params")
            if not runbook_id:
                return self._json_response({"error": "Missing 'runbook_id'"}, 400)
            try:
                res = client.execute_runbook(runbook_id, params=params)
                return self._json_response(res)
            except Exception as e:
                return self._json_response({"error": str(e)}, 500)

        elif path == "/api/v1/benchmark":
            iterations = payload.get("iterations", 5)
            res = orchestrator.benchmark_pipeline(iterations=iterations)
            return self._json_response(res)

        elif path == "/api/v1/do-everything":
            manifest = orchestrator.do_everything()
            return self._json_response(manifest)

        return self._json_response({"error": f"Endpoint not found: {path}"}, 404)


def find_free_port(start_port: int = 8769) -> int:
    port = start_port
    while port < start_port + 50:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
        port += 1
    return start_port


def main():
    global client, orchestrator
    parser = argparse.ArgumentParser(description="PowerShell Autonomous API Server & Cockpit Bridge")
    parser.add_argument("--port", type=int, default=8769, help="HTTP listening port (default: 8769)")
    parser.add_argument("--mock", action="store_true", help="Force mock simulation mode")
    args = parser.parse_args()

    config = PowerShellConfig(mock_mode=args.mock)
    client = PowerShellClient(config)
    orchestrator = PowerShellOrchestrator(client)

    port = find_free_port(args.port)
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, PowerShellApiHandler)

    print("=" * 65)
    print(f" POWERSHELL AUTONOMOUS COCKPIT & API SERVER")
    print("=" * 65)
    print(f" Cockpit UI:  http://localhost:{port}/")
    print(f" REST API:    http://localhost:{port}/api/v1/telemetry")
    print(f" Mode:        {'SIMULATION' if args.mock else 'LIVE HOST & FALLBACK'}")
    print(" Press Ctrl+C to terminate server.")
    print("=" * 65)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server shutting down cleanly.")
        httpd.server_close()


if __name__ == "__main__":
    main()
