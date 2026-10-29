"""
CS Video Courses REST API Server
Provides high-performance JSON endpoints and serves the Mission Control Cockpit.
Uses Python standard library (http.server, urllib, json, sqlite3) with zero third-party dependencies.
"""

import sys
import os
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, Any

from cs_courses_engine import CSCoursesEngine
from cs_courses_roadmaps import CSRoadmapsEngine

WORKSPACE_ROOT = Path(__file__).resolve().parent
DATA_DIR = WORKSPACE_ROOT / "data"
COCKPIT_HTML_PATH = WORKSPACE_ROOT / "cs_video_courses_cockpit.html"
ROADMAPS_JSON = DATA_DIR / "cs_role_roadmaps.json"
CURRICULA_DIR = WORKSPACE_ROOT / "docs" / "curricula"


class CSCoursesHandler(BaseHTTPRequestHandler):
    """HTTP request handler for CS Video Courses API and Cockpit."""

    def _set_headers(self, content_type: str = "application/json", status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(status=204)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)

        # Serve Cockpit UI
        if path in ["/", "/cockpit", "/index.html"]:
            if COCKPIT_HTML_PATH.exists():
                with open(COCKPIT_HTML_PATH, "r", encoding="utf-8") as f:
                    content = f.read()
                self._set_headers("text/html")
                self.wfile.write(content.encode("utf-8"))
            else:
                self._set_headers("text/plain", 404)
                self.wfile.write(b"Cockpit HTML not found.")
            return

        # API: Info & Summary Statistics
        if path == "/api/info":
            engine = CSCoursesEngine()
            stats = engine.get_summary_stats()
            self._set_headers()
            self.wfile.write(json.dumps(stats, ensure_ascii=False).encode("utf-8"))
            return

        # API: Filterable Courses Query
        if path == "/api/courses":
            engine = CSCoursesEngine()
            q = query_params.get("q", [""])[0]
            cat = query_params.get("category", [""])[0] or None
            subcat = query_params.get("subcategory", [""])[0] or None
            inst = query_params.get("institution", [""])[0] or None
            lvl = query_params.get("level", [""])[0] or None
            video_only = query_params.get("video_only", ["0"])[0] in ["1", "true", "True"]
            limit = int(query_params.get("limit", ["50"])[0])
            offset = int(query_params.get("offset", ["0"])[0])

            results = engine.search_courses(
                query=q,
                category=cat,
                subcategory=subcat,
                institution=inst,
                level=lvl,
                has_video_only=video_only,
                limit=limit,
                offset=offset,
            )

            response = {
                "count": len(results),
                "limit": limit,
                "offset": offset,
                "query": q,
                "category": cat,
                "institution": inst,
                "level": lvl,
                "courses": results,
            }
            self._set_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))
            return

        # API: Tracks
        if path == "/api/tracks":
            engine = CSCoursesEngine()
            stats = engine.get_summary_stats()
            self._set_headers()
            self.wfile.write(json.dumps(stats["tracks"], ensure_ascii=False).encode("utf-8"))
            return

        # API: Institutions
        if path == "/api/institutions":
            engine = CSCoursesEngine()
            stats = engine.get_summary_stats()
            self._set_headers()
            self.wfile.write(json.dumps(stats["institutions"], ensure_ascii=False).encode("utf-8"))
            return

        # API: Roadmaps
        if path == "/api/roadmaps":
            if not ROADMAPS_JSON.exists():
                builder = CSRoadmapsEngine()
                builder.build_all_roadmaps()
            with open(ROADMAPS_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._set_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return

        # API: Single Roadmap
        if path.startswith("/api/roadmaps/"):
            role_id = path.replace("/api/roadmaps/", "").strip().lower()
            if not ROADMAPS_JSON.exists():
                builder = CSRoadmapsEngine()
                builder.build_all_roadmaps()
            with open(ROADMAPS_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            match = next((r for r in data if r["role_id"] == role_id), None)
            if match:
                self._set_headers()
                self.wfile.write(json.dumps(match, ensure_ascii=False).encode("utf-8"))
            else:
                self._set_headers("application/json", 404)
                self.wfile.write(json.dumps({"error": f"Role '{role_id}' not found"}).encode("utf-8"))
            return

        # API: Raw Curriculum Markdown
        if path.startswith("/api/curricula/"):
            role_id = path.replace("/api/curricula/", "").strip().lower()
            md_file = CURRICULA_DIR / f"{role_id}.md"
            if md_file.exists():
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                self._set_headers("text/markdown")
                self.wfile.write(content.encode("utf-8"))
            else:
                self._set_headers("application/json", 404)
                self.wfile.write(json.dumps({"error": f"Curriculum markdown for '{role_id}' not found"}).encode("utf-8"))
            return

        # 404 Catch-All
        self._set_headers("application/json", 404)
        self.wfile.write(json.dumps({"error": "Endpoint not found", "path": path}).encode("utf-8"))

    def log_message(self, format, *args):
        # Concise logging
        sys.stderr.write(f"[CS-COURSES-API] {args[0]} - {args[1]}\n")


def run_server(host: str = "127.0.0.1", port: int = 8779):
    server = HTTPServer((host, port), CSCoursesHandler)
    print(f"\n=======================================================")
    print(f"  CS Video Courses API Server & Mission Control Cockpit")
    print(f"  Listening on: http://{host}:{port}/")
    print(f"  Cockpit URL : http://localhost:{port}/")
    print(f"=======================================================\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down CS Courses API server...")
        server.server_close()


if __name__ == "__main__":
    port = 8779
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port=port)
