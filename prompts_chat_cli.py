"""
prompts_chat_cli.py — Unified CLI & Local API Server for prompts.chat
=====================================================================
Interactive search, variable interpolation, quality auditing, and local
web server powering the Prompts.chat Visual Cockpit.
"""

from __future__ import annotations

import argparse
import http.server
import json
import os
import socketserver
import sys
import urllib.parse
from pathlib import Path
from typing import Any, Dict

from prompts_chat_engine import (
    QualityScorer,
    VariableExtractor,
    get_engine,
)

ROOT_DIR = Path(__file__).resolve().parent
COCKPIT_HTML_PATH = ROOT_DIR / "prompts_chat_cockpit.html"


class PromptsChatHttpHandler(http.server.BaseHTTPRequestHandler):
    """Handles REST API and Cockpit UI requests."""

    def log_message(self, format: str, *args: Any) -> None:
        # Suppress noisy logs during regular operation
        pass

    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def _send_json(self, data: Any, status: int = 200) -> None:
        payload = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)
        engine = get_engine()

        # Serve Cockpit UI at root
        if path in ("/", "/index.html", "/cockpit"):
            if not COCKPIT_HTML_PATH.exists():
                self.send_error(404, "prompts_chat_cockpit.html not found.")
                return
            html_bytes = COCKPIT_HTML_PATH.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_bytes)))
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(html_bytes)
            return

        # REST Endpoints
        if path == "/api/stats":
            self._send_json(engine.get_stats())
            return

        if path == "/api/skills":
            q = query_params.get("q", [""])[0]
            limit = int(query_params.get("limit", [20])[0])
            skills = engine.search_skills(q, limit=limit)
            self._send_json({"total": len(skills), "query": q, "skills": skills})
            return

        if path.startswith("/api/skill/"):
            skill_name = urllib.parse.unquote(path[len("/api/skill/"):])
            skill = engine.get_skill(skill_name)
            if skill:
                self._send_json(skill)
            else:
                self._send_json({"error": "Skill not found"}, status=404)
            return

        if path == "/api/book-languages":
            self._send_json({"languages": engine.get_book_languages()})
            return

        if path == "/api/book":
            lang = query_params.get("lang", ["en"])[0]
            self._send_json({"chapters": engine.get_book_chapters(lang=lang)})
            return

        if path.startswith("/api/book/"):
            chapter_slug = urllib.parse.unquote(path[len("/api/book/"):])
            lang = query_params.get("lang", ["en"])[0]
            chapter = engine.get_book_chapter(chapter_slug, lang=lang)
            if chapter:
                self._send_json(chapter)
            else:
                self._send_json({"error": "Chapter not found"}, status=404)
            return

        if path == "/api/search":
            q = query_params.get("q", [""])[0]
            cat = query_params.get("category", [None])[0]
            dev_str = query_params.get("for_devs", [None])[0]
            for_devs = True if dev_str == "1" or dev_str == "true" else (False if dev_str == "0" or dev_str == "false" else None)
            limit = int(query_params.get("limit", [50])[0])
            offset = int(query_params.get("offset", [0])[0])

            records, total = engine.search(query=q, category=cat, for_devs=for_devs, limit=limit, offset=offset)
            self._send_json({
                "total": total,
                "count": len(records),
                "offset": offset,
                "limit": limit,
                "results": [r.to_dict() for r in records]
            })
            return

        if path.startswith("/api/prompt/"):
            slug_or_act = urllib.parse.unquote(path[len("/api/prompt/"):])
            record = engine.get_by_slug(slug_or_act) or engine.get_by_act(slug_or_act)
            if record:
                self._send_json(record.to_dict())
            else:
                self._send_json({"error": "Prompt not found"}, status=404)
            return

        if path == "/api/random":
            cat = query_params.get("category", [None])[0]
            dev_str = query_params.get("for_devs", [None])[0]
            for_devs = True if dev_str == "1" or dev_str == "true" else None
            record = engine.get_random(for_devs=for_devs, category=cat)
            if record:
                self._send_json(record.to_dict())
            else:
                self._send_json({"error": "No prompt found matching filter"}, status=404)
            return

        self._send_json({"error": "Endpoint not found"}, status=404)

    def do_POST(self) -> None:
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        engine = get_engine()

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON body"}, status=400)
            return

        if path == "/api/fill":
            act = data.get("act", "")
            variables = data.get("variables", {})
            record = engine.get_by_act(act) or engine.get_by_slug(act)
            if not record:
                self._send_json({"error": "Prompt not found"}, status=404)
                return
            filled = VariableExtractor.interpolate(record.prompt, variables)
            self._send_json({
                "act": record.act,
                "original": record.prompt,
                "filled": filled,
                "variables": variables
            })
            return

        if path == "/api/quality":
            prompt = data.get("prompt", "")
            score, positives = QualityScorer.score(prompt)
            self._send_json({
                "quality_score": score,
                "strengths": positives,
                "char_count": len(prompt),
                "word_count": len(prompt.split())
            })
            return

        self._send_json({"error": "Endpoint not found"}, status=404)


def run_server(port: int = 8877) -> None:
    engine = get_engine()
    print(f"================================================================")
    print(f" prompts.chat Universal Cockpit & API Server")
    print(f" Serving 2,627 Prompts across 8 Categories & 1,155 Contributors")
    print(f" URL: http://localhost:{port}/")
    print(f" API Endpoints: /api/stats, /api/search, /api/prompt/:act, /api/random")
    print(f"================================================================")

    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), PromptsChatHttpHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down prompts.chat server.")


def parse_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="prompts.chat CLI — Search, Fill, and Explore 2,627 Prompts")
    parser.add_argument("--search", "-s", type=str, help="Search prompts by keyword")
    parser.add_argument("--get", "-g", type=str, help="Get prompt by Act name or slug")
    parser.add_argument("--category", "-c", type=str, help="Filter search or random by category")
    parser.add_argument("--for-devs", action="store_true", help="Filter for developer prompts")
    parser.add_argument("--random", "-r", action="store_true", help="Get a random prompt")
    parser.add_argument("--fill", type=str, help="Act name to fill with variables")
    parser.add_argument("--vars", nargs="*", help="Variables to fill in KEY=VALUE format")
    parser.add_argument("--quality", type=str, help="Calculate prompt quality score")
    parser.add_argument("--book", nargs="?", const="list", type=str, help="Read or list chapters from The Interactive Book of Prompting")
    parser.add_argument("--export-json", nargs="?", const="data/prompts_chat_enriched.json", type=str, help="Export all enriched prompts to JSON")
    parser.add_argument("--search-skills", type=str, help="Search across the 3,841+ installed agent skills")
    parser.add_argument("--get-skill", type=str, help="Get instructions and file manifest for an installed agent skill")
    parser.add_argument("--stats", action="store_true", help="Print prompt library statistics")
    parser.add_argument("--sync", action="store_true", help="Sync database from CSV")
    parser.add_argument("--force", action="store_true", help="Force sync database")
    parser.add_argument("--serve", nargs="?", const=8877, type=int, help="Start Cockpit HTTP Server on specified port (default: 8877)")
    return parser.parse_args()


def main() -> None:
    args = parse_cli_args()
    engine = get_engine()

    if args.sync or args.force:
        count = engine.sync(force=args.force)
        print(f"Successfully synced {count} prompts into SQLite database.")
        return

    if args.export_json:
        out = engine.export_enriched_json(Path(args.export_json))
        print(f"Exported {engine.count():,} enriched prompts to: {out}")
        return

    if args.search_skills:
        skills = engine.search_skills(args.search_skills, limit=15)
        print(f"\nFound {len(skills)} skills matching '{args.search_skills}':")
        for idx, s in enumerate(skills, 1):
            desc = s["description"][:100] + "..." if len(s["description"]) > 100 else s["description"]
            print(f"{idx:2}. {s['name']}")
            if desc:
                print(f"    {desc}")
        print()
        return

    if args.get_skill:
        skill = engine.get_skill(args.get_skill)
        if skill:
            print(f"\nSkill: {skill['name']}")
            print(f"Path:  {skill['path']}")
            print(f"Files: {', '.join(skill['files'])}\n")
            print("--- SKILL.md ---")
            print(skill["content"][:1500] + ("\n... [truncated]" if len(skill["content"]) > 1500 else ""))
            print("----------------\n")
        else:
            print(f"Skill '{args.get_skill}' not found.")
        return

    if args.stats:
        stats = engine.get_stats()
        print("\n--- prompts.chat Library Census ---")
        print(f"Total Prompts:        {stats['total_prompts']:,}")
        print(f"Developer Prompts:    {stats['developer_prompts']:,}")
        print(f"Average Quality:      {stats['average_quality']}/100")
        print(f"Unique Contributors:  {stats['unique_contributors']:,}")
        print("\nCategories:")
        for cat, cnt in stats["categories"].items():
            print(f"  - {cat:25}: {cnt:,}")
        print("\nTop Contributors:")
        for c in stats["top_contributors"]:
            print(f"  - {c['name']:25}: {c['count']:,} prompts")
        print()
        return

    if args.serve is not None:
        run_server(args.serve)
        return

    if args.book:
        if args.book == "list":
            chapters = engine.get_book_chapters()
            print("\n--- The Interactive Book of Prompting (31 Chapters) ---")
            for idx, ch in enumerate(chapters, 1):
                print(f"{idx:2}. [{ch['slug']}] {ch['title']}")
            print("\nTo read a chapter: python prompts_chat_cli.py --book <slug>")
            print("Example: python prompts_chat_cli.py --book 01-understanding-ai-models\n")
        else:
            ch = engine.get_book_chapter(args.book)
            if ch:
                print(f"\n========================================================")
                print(f" CHAPTER: {ch['title']}")
                print(f" Slug: {ch['slug']} | Words: {ch['word_count']:,}")
                print(f"========================================================\n")
                print(ch["content"])
                print(f"\n========================================================\n")
            else:
                print(f"Chapter '{args.book}' not found. Use --book list to view all chapters.")
        return

    if args.random:
        rec = engine.get_random(for_devs=True if args.for_devs else None, category=args.category)
        if rec:
            print(f"\n[RANDOM PROMPT] {rec.act} (Quality: {rec.quality_score}/100 | Category: {rec.category})")
            print(f"Contributor: {rec.contributor or 'Community'}")
            print("-" * 60)
            print(rec.prompt)
            print("-" * 60)
        else:
            print("No matching prompt found.")
        return

    if args.get:
        rec = engine.get_by_act(args.get) or engine.get_by_slug(args.get)
        if rec:
            print(f"\nAct:         {rec.act}")
            print(f"Slug:        {rec.slug}")
            print(f"Category:    {rec.category}")
            print(f"Archetype:   {rec.archetype}")
            print(f"Quality:     {rec.quality_score}/100")
            print(f"For Devs:    {rec.for_devs}")
            print(f"Contributor: {rec.contributor or 'Community'}")
            if rec.variables:
 