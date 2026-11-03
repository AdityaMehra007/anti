"""
OMEGA GitHub Marketplace Autonomous REST API Server
===================================================
High-throughput, lightweight REST API server providing sub-millisecond search,
category filtering, workflow synthesis, security auditing, graph topology,
and 12-phase sovereign lifecycle execution.

Supreme Constitution: OMEGA_CONSTITUTION.md
Operational Mode: Version OMNI-X / Production Engineering Mode
"""

import sys
import os

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import json
import urllib.parse
from typing import Any, Dict, List, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from github_marketplace_orchestrator import (
    engine,
    WorkflowSynthesizer,
    WorkflowSecurityAuditor,
    MANIFEST_JSON_PATH,
    MARKETPLACE_JSON_PATH,
    GRAPH_JSON_PATH
)

DEFAULT_PORT = 8783
COCKPIT_HTML_PATH = Path(r"E:\anti\github_marketplace_cockpit.html")


class GitHubMarketplaceAPIHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def _send_json(self, data: Any, status: int = 200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html_content: str, status: int = 200):
        body = html_content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)

        # Serve Cockpit
        if path in ["/", "/cockpit", "/index.html"]:
            if COCKPIT_HTML_PATH.exists():
                with open(COCKPIT_HTML_PATH, "r", encoding="utf-8", errors="replace") as f:
                    self._send_html(f.read())
            else:
                self._send_html("<h1>GitHub Marketplace Mission Control Cockpit initializing...</h1>")
            return

        # /api/health
        if path == "/api/health":
            self._send_json({
                "status": "healthy",
                "service": "OMEGA GitHub Marketplace Sovereign API",
                "port": DEFAULT_PORT,
                "total_items": len(engine.items),
                "total_categories": len(engine.categories)
            })
            return

        # /api/telemetry
        if path == "/api/telemetry":
            total_items = len(engine.items)
            actions_count = sum(1 for it in engine.items.values() if it.type == "action")
            apps_count = sum(1 for it in engine.items.values() if it.type == "app")
            verified_count = sum(1 for it in engine.items.values() if it.verified_creator)
            s_tier = sum(1 for it in engine.items.values() if it.tier == "S")
            avg_score = round(sum(it.security_score for it in engine.items.values()) / max(1, total_items), 1)

            self._send_json({
                "total_items": total_items,
                "total_actions": actions_count,
                "total_apps": apps_count,
                "verified_creators": verified_count,
                "s_tier_flagships": s_tier,
                "average_security_score": avg_score,
                "total_categories": len(engine.categories),
                "categories": list(engine.categories.values())
            })
            return

        # /api/categories
        if path == "/api/categories":
            self._send_json(list(engine.categories.values()))
            return

        # /api/search
        if path == "/api/search":
            q = query_params.get("q", [""])[0]
            cat = query_params.get("category", [None])[0]
            itype = query_params.get("type", [None])[0]
            verified = query_params.get("verified", ["false"])[0].lower() in ["true", "1", "yes"]
            limit = int(query_params.get("limit", [50])[0])

            results = engine.search(
                query=q,
                category=cat,
                item_type=itype,
                verified_only=verified,
                limit=limit
            )
            self._send_json({
                "query": q,
                "count": len(results),
                "results": results
            })
            return

        # /api/actions
        if path == "/api/actions":
            limit = int(query_params.get("limit", [50])[0])
            actions = [it.to_dict() for it in engine.items.values() if it.type == "action"]
            actions = sorted(actions, key=lambda x: x["stars"], reverse=True)[:limit]
            self._send_json({"count": len(actions), "actions": actions})
            return

        # /api/apps
        if path == "/api/apps":
            limit = int(query_params.get("limit", [50])[0])
            apps = [it.to_dict() for it in engine.items.values() if it.type == "app"]
            apps = sorted(apps, key=lambda x: x["stars"], reverse=True)[:limit]
            self._send_json({"count": len(apps), "apps": apps})
            return

        # /api/items/{slug}
        if path.startswith("/api/items/"):
            slug = path[len("/api/items/"):]
            item = engine.get_item(slug)
            if item:
                self._send_json(item)
            else:
                self._send_json({"error": "Item not found", "slug": slug}, status=404)
            return

        # /api/graph
        if path == "/api/graph":
            self._send_json({
                "nodes": [{"id": it.id, "name": it.name, "type": it.type, "category": it.category} for it in engine.items.values()],
                "edges": engine.graph_edges
            })
            return

        # /api/manifest or /api/lifecycle
        if path in ["/api/manifest", "/api/lifecycle"]:
            if MANIFEST_JSON_PATH.exists():
                with open(MANIFEST_JSON_PATH, "r", encoding="utf-8") as f:
                    self._send_json(json.load(f))
            else:
                self._send_json(engine.do_everything())
            return

        self._send_json({"error": "Endpoint not found", "path": path}, status=404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_length).decode("utf-8")

        try:
            payload = json.loads(post_body) if post_body else {}
        except Exception:
            payload = {}

        # POST /api/generate-workflow
        if path == "/api/generate-workflow":
            stack = payload.get("stack", "python")
            options = {
                "pin_sha": payload.get("pin_sha", True),
                "security_scan": payload.get("security_scan", True),
                "cache": payload.get("cache", True)
            }
            yaml_code = WorkflowSynthesizer.synthesize(stack, options)
            self._send_json({
                "stack": stack,
                "options": options,
                "yaml": yaml_code
            })
            return

        # POST /api/audit-workflow
        if path == "/api/audit-workflow":
            yaml_code = payload.get("yaml", "")
            report = WorkflowSecurityAuditor.audit_yaml(yaml_code)
            self._send_json(report)
            return

        # POST /api/lifecycle (Re-run lifecycle)
        if path in ["/api/lifecycle", "/api/do-everything"]:
            manifest = engine.do_everything()
            self._send_json(manifest)
            return

        self._send_json({"error": "POST endpoint not found", "path": path}, status=404)

    def log_message(self, format, *args):
        # Quiet standard HTTP log to keep output readable
        pass


def run_server(port: int = DEFAULT_PORT):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, GitHubMarketplaceAPIHandler)
    print(f"[+] OMEGA GitHub Marketplace API Server listening on http://127.0.0.1:{port}")
    print(f"[+] Mission Control Cockpit: http://127.0.0.1:{port}/cockpit")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server shutdown.")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    run_server(port)
