"""
OMEGA Awesome Universe Universal CLI
====================================
Command-line interface for exploring, searching, linting, and orchestrating
GitHub community-curated Awesome Lists and Frontier AI ecosystems.

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

import argparse
import json
from pathlib import Path
from awesome_orchestrator import engine, AwesomeManifestoLinter, SQLITE_DB_PATH, MANIFEST_JSON_PATH


def cmd_info(args):
    print("=" * 72)
    print("  OMEGA AWESOME UNIVERSE — SOVEREIGN ORCHESTRATION TELEMETRY")
    print("=" * 72)
    print(f"  Total Curated Lists:     {len(engine.lists)}")
    print(f"  Knowledge Categories:    {len(engine.categories)}")
    s_tier = sum(1 for l in engine.lists.values() if l.tier == 'S')
    a_tier = sum(1 for l in engine.lists.values() if l.tier == 'A')
    frontier = sum(1 for l in engine.lists.values() if l.is_frontier_ai)
    print(f"  S-Tier Flagships:        {s_tier}")
    print(f"  A-Tier Benchmarks:       {a_tier}")
    print(f"  Frontier AI & Agents:    {frontier}")
    print(f"  SQLite FTS5 DB:          {SQLITE_DB_PATH}")
    print(f"  Sovereign Manifest:      {MANIFEST_JSON_PATH}")
    print("-" * 72)
    print("  Top 5 Categories by Density:")
    top_cats = sorted(engine.categories.values(), key=lambda x: x["list_count"], reverse=True)[:5]
    for c in top_cats:
        print(f"   • {c['name']:<30} [{c['list_count']:>3} lists]")
    print("=" * 72)


def cmd_categories(args):
    print("=" * 72)
    print(f"  AWESOME UNIVERSE CATEGORIES ({len(engine.categories)})")
    print("=" * 72)
    for c in sorted(engine.categories.values(), key=lambda x: x["name"]):
        print(f"  [{c['list_count']:>3} lists]  {c['name']:<35} (slug: {c['slug']})")
    print("=" * 72)


def cmd_category(args):
    slug = args.slug.lower()
    cat = next((c for c in engine.categories.values() if c["slug"] == slug or c["name"].lower() == slug), None)
    if not cat:
        print(f"[-] Category '{args.slug}' not found. Use 'awesome_cli.py categories' to list.")
        return

    print("=" * 72)
    print(f"  CATEGORY: {cat['name'].upper()} ({cat['list_count']} lists)")
    print("=" * 72)
    for lid in cat["lists"]:
        if lid in engine.lists:
            item = engine.lists[lid]
            tier_badge = f"[{item.tier}-TIER]"
            print(f"  • {item.name:<25} {tier_badge:<8} ⭐ {item.stars:<6}")
            print(f"    {item.description}")
            print(f"    URL: {item.url}")
            print()
    print("=" * 72)


def cmd_search(args):
    query = " ".join(args.query)
    results = engine.search(query, category_slug=args.category, limit=args.limit)
    print("=" * 72)
    print(f"  SEARCH RESULTS FOR: '{query}' (Found {len(results)})")
    print("=" * 72)
    for r in results:
        frontier_tag = " [FRONTIER AI]" if r.get("is_frontier_ai") else ""
        print(f"  ⭐ {r.get('stars', 0):<6} [{r.get('tier', 'B')}-TIER]{frontier_tag} {r.get('name')}")
        print(f"     Category: {r.get('category')}")
        print(f"     Desc:     {r.get('description')}")
        print(f"     URL:      {r.get('url')}")
        print()
    print("=" * 72)


def cmd_list(args):
    lid = args.id.lower()
    item = engine.lists.get(lid)
    if not item:
        # Try search by name
        item = next((l for l in engine.lists.values() if l.name.lower() == lid or l.repo.lower() == lid), None)

    if not item:
        print(f"[-] List '{args.id}' not found.")
        return

    print("=" * 72)
    print(f"  AWESOME LIST DOSSIER: {item.name.upper()}")
    print("=" * 72)
    print(f"  ID:               {item.id}")
    print(f"  Repository:       {item.repo or 'External'}")
    print(f"  Category:         {item.category} ({item.category_slug})")
    print(f"  Tier Rating:      {item.tier}-Tier")
    print(f"  Estimated Stars:  ⭐ {item.stars:,}")
    print(f"  Frontier AI:      {'Yes' if item.is_frontier_ai else 'No'}")
    print(f"  Manifesto Score:  {item.manifesto_score}/100")
    print(f"  Canonical URL:    {item.url}")
    print(f"  Description:      {item.description}")
    if item.related_lists:
        print(f"  Related Lists:    {', '.join(item.related_lists)}")
    print("=" * 72)


def cmd_frontier(args):
    frontier_items = [l for l in engine.lists.values() if l.is_frontier_ai]
    print("=" * 72)
    print(f"  FRONTIER AI & AGENTIC ECOSYSTEMS ({len(frontier_items)})")
    print("=" * 72)
    for f in frontier_items:
        print(f"  • {f.name:<25} [{f.tier}-TIER] ⭐ {f.stars:<6} | {f.repo}")
        print(f"    {f.description}")
        print(f"    Topics: {', '.join(f.topics)}")
        print(f"    URL:    {f.url}")
        print()
    print("=" * 72)


def cmd_lint(args):
    path_or_text = args.target
    if os.path.exists(path_or_text):
        with open(path_or_text, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        repo_name = Path(path_or_text).stem
    else:
        content = path_or_text
        repo_name = args.repo_name or "awesome-custom"

    res = AwesomeManifestoLinter.lint_markdown(content, repo_name=repo_name)
    print("=" * 72)
    print(f"  AWESOME MANIFESTO LINT REPORT — {repo_name}")
    print("=" * 72)
    print(f"  Compliance Status:    {res['status']}")
    print(f"  Manifesto Score:      {res['manifesto_score']}/100")
    print(f"  Checks Passed:        {res['checks_passed']} / {res['total_checks']}")
    print(f"  Entries Inspected:    {res['total_entries_inspected']}")
    print("-" * 72)
    if res["issues"]:
        print("  Issues & Warnings Detected:")
        for idx, iss in enumerate(res["issues"], 1):
            badge = f"[{iss['severity']}]"
            print(f"   {idx}. {badge:<8} Rule: {iss['rule']}")
            print(f"      {iss['message']}")
    else:
        print("  [+] Congratulations! Zero lint violations. Meets Awesome Manifesto.")
    print("=" * 72)


def cmd_graph(args):
    g = engine.get_graph()
    print("=" * 72)
    print("  AWESOME CROSS-CATEGORY GRAPH TOPOLOGY")
    print("=" * 72)
    print(f"  Total Graph Nodes:    {g['total_nodes']}")
    print(f"  Total Directed Links: {g['total_links']}")
    cat_nodes = sum(1 for n in g["nodes"] if n["type"] == "category")
    list_nodes = sum(1 for n in g["nodes"] if n["type"] == "list")
    print(f"  Category Hubs:        {cat_nodes}")
    print(f"  High-Tier Lists:      {list_nodes}")
    print("=" * 72)


def cmd_export(args):
    print("[*] Exporting Awesome Universe to JSON, SQLite, CSV, and Markdown...")
    engine.export_all()
    print("[+] Export completed successfully.")


def cmd_do_everything(args):
    print("=" * 72)
    print("  EXECUTING OMEGA 12-PHASE SOVEREIGN AWESOME LIFECYCLE")
    print("=" * 72)
    manifest = engine.do_everything()
    for p in manifest["phases"]:
        status_sym = "[+]" if p["status"] == "PASSED" else "[-]"
        print(f"  {status_sym} Phase {p['phase']:>2}: {p['name']:<50} ({p['elapsed_seconds']}s)")
    print("-" * 72)
    print(f"  Execution ID:    {manifest['execution_id']}")
    print(f"  Overall Status:  {manifest['overall_status']}")
    print(f"  Total Duration:  {manifest['total_elapsed_seconds']}s")
    print(f"  Manifest Path:   {MANIFEST_JSON_PATH}")
    print("=" * 72)


def cmd_serve(args):
    from awesome_api_server import run_server
    port = args.port or 8782
    run_server(port=port)


def main():
    parser = argparse.ArgumentParser(description="OMEGA Awesome Universe Universal CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # info
    subparsers.add_parser("info", help="Display universe telemetry and category stats")

    # categories
    subparsers.add_parser("categories", help="List all 29 categories")

    # category
    cat_parser = subparsers.add_parser("category", help="List all items in a category")
    cat_parser.add_argument("slug", help="Category slug or name")

    # search
    search_parser = subparsers.add_parser("search", help="Full-text search across lists")
    search_parser.add_argument("query", nargs="+", help="Keywords to search")
    search_parser.add_argument("--category", "-c", help="Filter by category slug")
    search_parser.add_argument("--limit", "-n", type=int, default=20, help="Max results")

    # list
    list_parser = subparsers.add_parser("list", help="Get details for a specific awesome list")
    list_parser.add_argument("id", help="List id, name, or repo slug")

    # frontier
    subparsers.add_parser("frontier", help="List Frontier AI, Autonomous Agents, and MCP lists")

    # lint
    lint_parser = subparsers.add_parser("lint", help="Lint markdown against Awesome Manifesto")
    lint_parser.add_argument("target", help="File path or markdown string to lint")
    lint_parser.add_argument("--repo-name", help="Repository slug (e.g. awesome-mytech)")

    # graph
    subparsers.add_parser("graph", help="Show graph topology statistics")

    # export
    subparsers.add_parser("export", help="Export universe datasets")

    # do-everything
    subparsers.add_parser("do-everything", help="Execute 12-phase sovereign lifecycle")

    # serve
    serve_parser = subparsers.add_parser("serve", help="Run local REST API server and Mission Control Cockpit")
    serve_parser.add_argument("--port", "-p", type=int, default=8782, help="Port to listen on (default: 8782)")

    args = parser.parse_args()

    if not args.command:
        cmd_info(args)
        return

    commands = {
        "info": cmd_info,
        "categories": cmd_categories,
        "category": cmd_category,
        "search": cmd_search,
        "list": cmd_list,
        "frontier": cmd_frontier,
        "lint": cmd_lint,
        "graph": cmd_graph,
        "export": cmd_export,
        "do-everything": cmd_do_everything,
        "serve": cmd_serve
    }

    cmd_fn = commands.get(args.command)
    if cmd_fn:
        cmd_fn(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
