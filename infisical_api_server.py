#!/usr/bin/env python3
"""
Infisical Autonomous Local REST API Server & Cockpit Bridge
===========================================================
Zero-dependency HTTP REST & Static Server serving the Infisical Mission Control Cockpit
and exposing real-time endpoints for secrets, leak scanning, dynamic leases, PKI/CA,
cloud syncing, RBAC workflows, and cryptographic audit blockchain verification.

Default Port: 8772
Usage:
    python infisical_api_server.py [--port 8772]
"""

from __future__ import annotations

import os
import sys
import json
import argparse
from typing import Any, Dict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from infisical_orchestrator import InfisicalClient, InfisicalOrchestrator, InfisicalConfig

client = InfisicalClient()
orchestrator = InfisicalOrchestrator(client)


class InfisicalApiHandler(SimpleHTTPRequestHandler):
    """HTTP request handler for Infisical REST API and static Cockpit."""

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def _json_response(self, data: Any, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def _parse_body(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        body = self.rfile.read(length).decode("utf-8")
        try:
            return json.loads(body)
        except Exception:
            return {}

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # Route root or html to cockpit
        if path in ("/", "/index.html", "/cockpit"):
            cockpit_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "infisical_control_cockpit.html")
            if os.path.exists(cockpit_file):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(cockpit_file, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self._json_response({"error": "Cockpit HTML file not found"}, 404)
                return

        # -------------------------------------------------------------
        # REST API Routes
        # -------------------------------------------------------------
        if path in ("/api/status", "/api/telemetry"):
            self._json_response(client.get_telemetry())

        elif path == "/api/projects":
            self._json_response(client.list_projects())

        elif path == "/api/secrets":
            env = query.get("env", ["production"])[0]
            pid = query.get("project_id", ["proj-omega-core-001"])[0]
            sec_path = query.get("path", ["/"])[0]
            reveal = query.get("reveal", ["false"])[0].lower() in ("true", "1")
            self._json_response(client.list_secrets(project_id=pid, environment=env, secret_path=sec_path, reveal_values=reveal))

        elif path == "/api/secrets/get":
            key = query.get("key", [""])[0]
            env = query.get("env", ["production"])[0]
            pid = query.get("project_id", ["proj-omega-core-001"])[0]
            sec_path = query.get("path", ["/"])[0]
            res = client.get_secret(key, project_id=pid, environment=env, secret_path=sec_path)
            if res:
                self._json_response(res)
            else:
                self._json_response({"error": f"Secret {key} not found"}, 404)

        elif path == "/api/scan/workspace":
            dir_to_scan = query.get("path", ["."])[0]
            self._json_response(client.scan_workspace_for_leaks(dir_to_scan))

        elif path == "/api/dynamic/leases":
            self._json_response(client.list_dynamic_leases())

        elif path == "/api/pki/cas":
            self._json_response(client.list_certificate_authorities())

        elif path == "/api/pki/certs":
            self._json_response(client.list_certificates())

        elif path == "/api/integrations":
            self._json_response(client.list_integrations())

        elif path == "/api/access-requests":
            self._json_response(client.list_access_requests())

        elif path == "/api/audit":
            limit = int(query.get("limit", [50])[0])
            self._json_response(client.list_audit_logs(limit=limit))

        elif path == "/api/audit/verify":
            self._json_response(client.verify_audit_ledger())

        elif path == "/api/manifest":
            manifest_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "omega", "data", "infisical_do_everything_manifest.json")
            if os.path.exists(manifest_path):
                with open(manifest_path, "r", encoding="utf-8") as f:
                    self._json_response(json.load(f))
            else:
                self._json_response({"error": "Manifest not generated yet. Run /api/do-everything"}, 404)

        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._parse_body()

        if path == "/api/projects":
            name = body.get("name", "New Project")
            slug = body.get("slug", "new-proj")
            desc = body.get("description", "")
            res = client.create_project(name, slug, desc)
            self._json_response(res, 201)

        elif path == "/api/secrets/set":
            key = body.get("key")
            val = body.get("value")
            pid = body.get("project_id", "proj-omega-core-001")
            env = body.get("environment", "production")
            sec_path = body.get("path", "/")
            comment = body.get("comment", "")
            tags = body.get("tags", [])
            if not key or val is None:
                self._json_response({"error": "Missing key or value"}, 400)
                return
            sec = client.set_secret(key, val, project_id=pid, environment=env, secret_path=sec_path, comment=comment, tags=tags)
            self._json_response(sec)

        elif path == "/api/secrets/delete":
            key = body.get("key")
            pid = body.get("project_id", "proj-omega-core-001")
            env = body.get("environment", "production")
            sec_path = body.get("path", "/")
            ok = client.delete_secret(key, project_id=pid, environment=env, secret_path=sec_path)
            self._json_response({"deleted": ok})

        elif path == "/api/secrets/rollback":
            key = body.get("key")
            ver = body.get("version", 1)
            pid = body.get("project_id", "proj-omega-core-001")
            env = body.get("environment", "production")
            sec_path = body.get("path", "/")
            res = client.rollback_secret(key, int(ver), project_id=pid, environment=env, secret_path=sec_path)
            if res:
                self._json_response(res)
            else:
                self._json_response({"error": f"Version {ver} not found for {key}"}, 404)

        elif path == "/api/scan":
            text = body.get("text", "")
            label = body.get("label", "<api_input>")
            matches = client.scan_content_for_leaks(text, label=label)
            self._json_response(matches)

        elif path == "/api/dynamic/create":
            name = body.get("name", "db-ephemeral")
            engine = body.get("engine", "postgres")
            ttl = int(body.get("ttl", 3600))
            lease = client.create_dynamic_secret_lease(name, engine_type=engine, ttl_seconds=ttl)
            self._json_response(lease, 201)

        elif path == "/api/dynamic/revoke":
            lease_id = body.get("lease_id")
            ok = client.revoke_dynamic_lease(lease_id)
            self._json_response({"revoked": ok})

        elif path == "/api/pki/issue":
            cn = body.get("common_name", "client.internal")
            sans = body.get("sans", [cn])
            days = int(body.get("days", 90))
            ca_id = body.get("ca_id")
            cert = client.issue_tls_certificate(cn, sans=sans, ca_id=ca_id, validity_days=days)
            self._json_response(cert, 201)

        elif path == "/api/pki/revoke":
            serial = body.get("serial")
            reason = body.get("reason", "KeyCompromise")
            ok = client.revoke_certificate(serial, reason=reason)
            self._json_response({"revoked": ok})

        elif path == "/api/integrations/sync":
            integ_id = body.get("id")
            res = client.sync_integration(integ_id)
            self._json_response(res)

        elif path == "/api/access-requests/create":
            role = body.get("role", "Break-Glass Operator")
            reason = body.get("reason", "Emergency mitigation")
            duration = int(body.get("duration", 60))
            env = body.get("environment", "production")
            requester = body.get("requester", "api-user")
            req = client.create_access_request(requester, role, reason, duration_minutes=duration, environment=env)
            self._json_response(req, 201)

        elif path == "/api/access-requests/approve":
            req_id = body.get("request_id")
            approver = body.get("approver", "security-lead")
            req = client.approve_access_request(req_id, approver=approver)
            self._json_response(req)

        elif path == "/api/do-everything":
            manifest = orchestrator.do_everything()
            self._json_response(manifest)

        else:
            self._json_response({"error": "Unknown API endpoint"}, 404)


def is_port_free(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def find_free_port(preferred: int = 8772, max_attempts: int = 10) -> int:
    for p in range(preferred, preferred + max_attempts):
        if is_port_free(p):
            return p
    return preferred


def run_server(port: int = 8772):
    chosen_port = find_free_port(port)
    server_address = ("", chosen_port)
    httpd = HTTPServer(server_address, InfisicalApiHandler)
    logger.info("=== OMEGA INFISICAL REST API SERVER ACTIVE ===")
    logger.info("Port            : %d", chosen_port)
    logger.info("Mission Cockpit : http://localhost:%d/", chosen_port)
    logger.info("Telemetry API   : http://localhost:%d/api/status", chosen_port)
    logger.info("==============================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Infisical API Server stopped.")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Infisical Autonomous Local REST API Server")
    parser.add_argument("--port", type=int, default=int(os.getenv("INFISICAL_API_PORT", "8772")), help="HTTP server port")
    args = parser.parse_args()
    run_server(args.port)
