"""
OMEGA Awesome Universe Autonomous REST API Server
==================================================
High-throughput, lightweight REST API server providing sub-millisecond search,
category filtering, Awesome Manifesto linting, graph topology, and lifecycle execution.

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
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from awesome_orchestrator import engine, AwesomeManifestoLinter, MANIFEST_JSON_PATH

DEFAULT_PORT = 8782
COCKPIT_HTML_PATH = Path(r"E:\anti\awesome_control_cockpit.html")


class AwesomeAPIHandler(BaseHTTPRequestHandler):
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
                self._send_json({"error": "Cockpit HTML not generated yet"}, status=404)
            return

        # /api/info
        if path == "/api/info":
            s_tier = sum(1 for l in engine.lists.values() if l.tier == "S")
            a_tier = sum(1 for l in engine.lists.values() if l.tier == "A")
            frontier = sum(1 for l in engine.lists.values() if l.is_frontier_ai)
            self._send_json({
                "status": "OPERATIONAL",
                "protocol": "OMEGA_AWESOME_UNIVERSE_V1",
                "upstream_hub": "https://github.com/topics/awesome",
                "upstream_readme": "https://github.com/sindresorhus/awesome",
                "total_lists": len(engine.lists),
                "total_categories": len(engine.categories),
                "s_tier_count": s_tier,
                "a_tier_count": a_tier,
                "frontier_ai_count": frontier,
                "indexed_db": str(engine.compile_sqlite())
            })
            return

        # /api/categories
        if path == "/api/categories":
            cats = [
                {
                    "name": c["name"],
                    "slug": c["slug"],
                    "icon": c["icon"],
                    "list_count": c["list_count"]
                }
                for c in sorted(engine.categories.values(), key=lambda x: x["name"])
            ]
            self._send_json(cats)
            return

        # /api/category/<slug>
        if path.startswith("/api/category/"):
            slug = path[len("/api/category/"):].strip()
            cat = next((c for c in engine.categories.values() if c["slug"] == slug or c["name"].lower() == slug.lower()), None)
            if not cat:
                self._send_json({"error": f"Category '{slug}' not found"}, status=404)
                return
            items = [engine.lists[lid].to_dict() for lid in cat["lists"] if lid in engine.lists]
            self._send_json({
                "category": cat["name"],
                "slug": cat["slug"],
                "icon": cat["icon"],
                "list_count": cat["list_count"],
                "lists": items
            })
            return

        # /api/search?q=<query>&category=<slug>&limit=<n>
        if path == "/api/search":
            q = query_params.get("q", [""])[0]
            cat_slug = query_params.get("category", [None])[0]
            limit = int(query_params.get("limit", [50])[0])
            results = engine.search(q, category_slug=cat_slug, limit=limit)
            self._send_json({
                "query": q,
                "category": cat_slug,
                "total_matched": len(results),
                "results": results
            })
            return

        # /api/lists
        if path == "/api/lists":
            tier = query_params.get("tier", [None])[0]
            limit = int(query_params.get("limit", [100])[0])
            items = list(engine.lists.values())
            if tier:
                items = [i for i in items if i.tier.upper() == tier.upper()]
            items.sort(key=lambda x: x.stars, reverse=True)
            self._send_json([i.to_dict() for i in items[:limit]])
            return

        # /api/list/<id>
        if path.startswith("/api/list/"):
            lid = path[len("/api/list/"):].strip()
            item = engine.lists.get(lid)
            if not item:
                item = next((l for l in engine.lists.values() if l.name.lower() == lid.lower() or l.repo.lower() == lid.lower()), None)
            if not item:
                self._send_json({"error": f"List '{lid}' not found"}, status=404)
                return
            self._send_json(item.to_dict())
            return

        # /api/frontier
        if path == "/api/frontier":
            frontier_items = [l.to_dict() for l in engine.lists.values() if l.is_frontier_ai]
            self._send_json(frontier_items)
            return

        # /api/graph
        if path == "/api/graph":
            self._send_json(engine.get_graph())
            return

        # /api/lifecycle
        if path == "/api/lifecycle":
            if MANIFEST_JSON_PATH.exists():
                with open(MANIFEST_JSON_PATH, "r", encoding="utf-8") as f:
                    self._send_json(json.load(f))
            else:
                self._send_json(engine.do_everything())
            return

        # /api/lint/sample
        if path == "/api/lint/sample":
            sample = (
                "# Awesome Sample\n\n[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)\n\n"
                "A curated list of awesome developer tools and resources.\n\n"
                "## Contents\n\n- [Developer Tools](#developer-tools)\n\n"
                "## Developer Tools\n\n- [ToolX](https://github.com/sample/toolx#readme) - Modern cloud dev tool."
            )
            report = AwesomeManifestoLinter.lint_markdown(sample, repo_name="awesome-sample")
            self._send_json(report)
            return

        self._send_json({"error": "Endpoint not found"}, status=404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_length).decode("utf-8")

        try:
            payload = json.loads(post_body) if post_body else {}
        except Exception:
            payload = {}

        # POST /api/lint
        if path == "/api/lint":
            md = payload.get("markdown", "")
            repo = payload.get("repo_name", "awesome-submission")
            report = AwesomeManifestoLinter.lint_markdown(md, repo_name=repo)
            self._send_json(report)
            return

        # POST /api/lifecycle (Trigger re-run)
        if path == "/api/lifecycle":
            manifest = engine.do_everything()
            self._send_json(manifest)
            return

        self._send_json({"error": "POST endpoint not found"}, status=404)

    def log_message(self, format, *args):
        # Quiet standard HTTP log to keep terminal clean
        pass


def run_server(port: int = DEFAULT_PORT):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, AwesomeAPIHandler)
    print(f"[+] OMEGA Awesome API Server listening on http://127.0.0.1:{port}")
    print(f"[+] Mission Control Cockpit: http://127.0.0.1:{port}/cockpit")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server shutdown.")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    run_server(port)
