#!/usr/bin/env python3
"""
n8n Enterprise Automation & Autonomous Agent CLI Engine
Search 560+ core nodes via SQLite FTS5, inspect 14 production workflows, trigger automation runs, and launch Web Command Center.
"""

import sys
import json
import sqlite3
import webbrowser
from pathlib import Path

DB_PATH = Path(r"e:\anti\data\n8n_arsenal.db")
CATALOG_PATH = Path(r"e:\anti\data\n8n_node_catalog.json")
WORKFLOWS_PATH = Path(r"e:\anti\data\n8n_active_workflows.json")
HTML_PATH = Path(r"e:\anti\n8n_command_center.html")

def search_nodes(query: str, limit: int = 10):
    if not DB_PATH.exists():
        print("[-] Database not found. Run index_n8n_db.py first.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    try:
        results = c.execute("""
            SELECT name, display_name, description, group_name
            FROM n8n_nodes_fts
            WHERE n8n_nodes_fts MATCH ?
            LIMIT ?
        """, (query, limit)).fetchall()
    except Exception:
        results = c.execute("""
            SELECT name, display_name, description, group_name
            FROM n8n_nodes
            WHERE name LIKE ? OR display_name LIKE ? OR description LIKE ?
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%", limit)).fetchall()
    conn.close()

    print(f"\nFound {len(results)} n8n node matches for '{query}':")
    print("=" * 80)
    for name, dname, desc, grp in results:
        print(f"• {dname} [{name}] ({grp})")
        if desc:
            clean_desc = desc[:180].replace("\n", " ").strip()
            print(f"    {clean_desc}...")
        print("-" * 80)

def list_workflows():
    if not WORKFLOWS_PATH.exists():
        print("[-] Workflows JSON not found.")
        return

    with open(WORKFLOWS_PATH, "r", encoding="utf-8") as f:
        wfs = json.load(f)

    print("\n14 ACTIVE OMEGA PRODUCTION WORKFLOWS:")
    print("=" * 75)
    for idx, w in enumerate(wfs, 1):
        print(f"[{idx:2d}] {w['name']:35s} ({w['nodes_count']:2d} nodes) -> {w['filename']}")
    print("=" * 75)

def open_dashboard():
    if HTML_PATH.exists():
        print(f"[+] Opening {HTML_PATH} in browser...")
        webbrowser.open(HTML_PATH.as_uri())
    else:
        print("[-] Dashboard HTML not found.")

def show_stats():
    if not CATALOG_PATH.exists() or not WORKFLOWS_PATH.exists():
        print("[-] Data files not found.")
        return

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        nodes = json.load(f)

    with open(WORKFLOWS_PATH, "r", encoding="utf-8") as f:
        wfs = json.load(f)

    from collections import Counter
    print("\nN8N ENTERPRISE AUTOMATION ECOSYSTEM METRICS:")
    print("=" * 60)
    print(f"Total Discovered Nodes: {len(nodes)}")
    print(f"Total Active Workflows: {len(wfs)}")
    print("\nNode Groups:")
    for grp, cnt in Counter(n.get("group", "utility") for n in nodes).most_common(8):
        print(f"  • {grp:25s}: {cnt:3d}")
    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print("""n8n Enterprise Automation CLI Engine
Usage:
  python n8n_engine.py --dashboard      # Launch Interactive Visual Web Command Center
  python n8n_engine.py --search <query>  # Fast FTS5 search across 560+ n8n core & community nodes
  python n8n_engine.py --workflows       # List 14 production OMEGA automation workflows
  python n8n_engine.py --stats           # Show catalog statistics & group distribution
        """)
        return

    cmd = sys.argv[1].lower()
    if cmd in ["--dashboard", "-d", "dashboard", "--web"]:
        open_dashboard()
    elif cmd in ["--search", "-s", "search"]:
        q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not q:
            print("Please specify a search query.")
            return
        search_nodes(q)
    elif cmd in ["--workflows", "-w", "workflows"]:
        list_workflows()
    elif cmd in ["--stats", "stats"]:
        show_stats()
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
