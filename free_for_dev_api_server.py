#!/usr/bin/env python3
"""
OMEGA Free-For-Dev Autonomous Local API Server
==============================================
High-speed REST API & Cockpit Host for the ripienaar/free-for-dev catalog.
Zero external pip dependencies (Python stdlib http.server with Threading).

Default Port: 8770
Endpoints:
  GET  /                          -> Serves Mission Control Cockpit
  GET  /cockpit                   -> Serves Mission Control Cockpit
  GET  /api/telemetry             -> High-level stats, quotas, and counts
  GET  /api/categories            -> All 57 categories with counts
  GET  /api/services              -> Filtered services list
  GET  /api/services/{id}         -> Single service detailed dossier
  GET  /api/stacks/archetypes     -> Curated zero-dollar stack archetypes
  GET  /api/stacks/{archetype}    -> Synthesize zero-dollar stack for archetype
  POST /api/stacks/architect      -> Dynamic zero-dollar stack architect
  GET  /api/compare?ids=a,b,c     -> Multi-provider head-to-head comparison
  POST /api/audit                 -> Architecture feasibility & quota auditor
  POST /api/cli                   -> Safe CLI execution bridge for web terminal
  POST /api/do-everything         -> Execute 12-phase sovereign lifecycle
"""

import sys
import os
import json
import urllib.parse
from datetime import datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, Any

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from free_for_dev_orchestrator import FreeForDevOrchestrator

WORKSPACE_DIR = Path(r"E:\anti")
COCKPIT_HTML_PATH = WORKSPACE_DIR / "free_for_dev_cockpit.html"
DEFAULT_PORT = 8771

ORCHESTRATOR = FreeForDevOrchestrator(auto_ingest=True)


class FreeForDevAPIHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def _send_json(self, data: Any, status: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html_path: Path):
        if not html_path.exists():
            self._send_json({"error": "Cockpit HTML not found"}, status=404)
            return
        content = html_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Cockpit Root
        if path in ["/", "/cockpit", "/index.html"]:
            self._send_html(COCKPIT_HTML_PATH)
            return

        # API Telemetry
        if path == "/api/telemetry":
            self._send_json(ORCHESTRATOR.get_telemetry())
            return

        # Categories
        if path == "/api/categories":
            self._send_json(ORCHESTRATOR.list_categories())
            return

        # Services List & Search
        if path == "/api/services":
            q = query.get("search", [""])[0]
            cat = query.get("category", [""])[0]
            no_card = query.get("no_card", ["false"])[0].lower() in ["true", "1", "yes"]
            tier = query.get("tier", [""])[0]
            role = query.get("role", [""])[0]
            limit = int(query.get("limit", [50])[0])

            results = ORCHESTRATOR.search_services(
                query=q, category=cat, no_card_only=no_card, tier=tier, role=role, limit=limit
            )
            self._send_json({
                "count": len(results),
                "query": q,
                "category": cat,
                "no_card": no_card,
                "services": results
            })
            return

        # Service Detail
        if path.startswith("/api/services/"):
            sid = path.split("/api/services/")[1].strip()
            srv = ORCHESTRATOR.get_service(sid)
            if srv:
                self._send_json(srv)
            else:
                self._send_json({"error": f"Service not found: {sid}"}, status=404)
            return

        # Stack Archetypes List
        if path == "/api/stacks/archetypes":
            archetypes = [
                {"id": "jamstack_saas", "name": "Fullstack Modern Jamstack & SaaS", "use_case": "B2B SaaS, Web Applications"},
                {"id": "ai_agent_platform", "name": "Autonomous AI Agentic Workflow Platform", "use_case": "Autonomous Agents, LLM Orchestration"},
                {"id": "mobile_app_backend", "name": "Cross-Platform Mobile App Cloud", "use_case": "iOS/Android Mobile Apps, Consumer Tech"},
                {"id": "microservices_api", "name": "High-Performance Event-Driven Microservices", "use_case": "High-volume APIs, Event Brokers"},
                {"id": "ecommerce_store", "name": "Headless E-Commerce & Storefront", "use_case": "Direct-to-Consumer storefronts"},
                {"id": "sovereign_no_card", "name": "Sovereign Zero-Credit-Card Fortress", "use_case": "Indie Hackers, Risk-Free Prototyping"},
                {"id": "analytics_data_pipeline", "name": "Serverless Analytics & Data Pipeline", "use_case": "BI Dashboards, ETL Pipelines"}
            ]
            self._send_json(archetypes)
            return

        # Specific Stack Archetype
        if path.startswith("/api/stacks/"):
            arch = path.split("/api/stacks/")[1].strip()
            stack = ORCHESTRATOR.architect_zero_dollar_stack(arch)
            self._send_json(stack)
            return

        # Head-to-Head Comparison
        if path == "/api/compare":
            ids_str = query.get("ids", [""])[0]
            ids = [i.strip() for i in ids_str.split(",") if i.strip()]
            if not ids:
                self._send_json({"error": "Missing 'ids' query parameter (e.g. ?ids=supabase,neon,turso)"}, status=400)
                return
            res = ORCHESTRATOR.compare_providers(ids)
            self._send_json(res)
            return

        self._send_json({"error": f"Not found: {path}"}, status=404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body_data = {}
        if content_length > 0:
            raw_body = self.rfile.read(content_length)
            try:
                body_data = json.loads(raw_body.decode("utf-8"))
            except Exception:
                body_data = {}

        # Architecture Feasibility Audit
        if path == "/api/audit":
            requirements = body_data.get("requirements", [])
            if isinstance(requirements, str):
                requirements = [r.strip() for r in requirements.split(",") if r.strip()]
            audit = ORCHESTRATOR.audit_architecture(requirements)
            self._send_json(audit)
            return

        # Dynamic Stack Synthesis
        if path == "/api/stacks/architect":
            archetype = body_data.get("archetype", "jamstack_saas")
            stack = ORCHESTRATOR.architect_zero_dollar_stack(archetype)
            self._send_json(stack)
            return

        # Execute 12-Phase Sovereign Lifecycle
        if path == "/api/do-everything":
            manifest = ORCHESTRATOR.execute_sovereign_lifecycle()
            self._send_json(manifest)
            return

        # Safe CLI Web Terminal Runner
        if path == "/api/cli":
            cmd = body_data.get("command", "").strip()
            if not cmd:
                self._send_json({"output": "No command provided."})
                return

            import io
            import contextlib
            from free_for_dev_cli import main as cli_main

            old_argv = sys.argv
            tokens = cmd.split()
            if tokens and tokens[0].lower() in ["ffd", "free_for_dev_cli.py", "python"]:
                tokens = [t for t in tokens if t not in ["python", "free_for_dev_cli.py"]]

            sys.argv = ["free_for_dev_cli.py"] + tokens
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                    cli_main()
                output_str = buf.getvalue()
            except SystemExit:
                output_str = buf.getvalue()
            except Exception as e:
                output_str = f"Error executing CLI: {e}\n{buf.getvalue()}"
            finally:
                sys.argv = old_argv

            self._send_json({"command": cmd, "output": output_str})
            return

        self._send_json({"error": f"Endpoint not found: {path}"}, status=404)

    def log_message(self, format, *args):
        # Concise quiet logging
        sys.stderr.write(f"[{datetime.now().strftime('%H:%M:%S')}] HTTP {args[0]} {args[1]}\n")


def run_server(port: int = DEFAULT_PORT):
    server_address = ("", port)
    try:
        httpd = ThreadingHTTPServer(server_address, FreeForDevAPIHandler)
        print(f"[*] OMEGA Free-For-Dev API Server & Cockpit live at: http://localhost:{port}")
        print(f"[*] Serving Cockpit UI: {COCKPIT_HTML_PATH}")
        print(f"[*] REST API base: http://localhost:{port}/api/telemetry")
        print("[*] Press Ctrl+C to terminate server.")
        httpd.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e) or e.errno == 10048:
            alt_port = port + 1
            print(f"[!] Port {port} in use, trying fallback port {alt_port}...")
            run_server(alt_port)
        else:
            raise e


if __name__ == "__main__":
    port_arg = DEFAULT_PORT
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port_arg = int(sys.argv[1])
    run_server(port_arg)
