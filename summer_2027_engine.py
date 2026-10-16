#!/usr/bin/env python3
"""
Summer 2027 Internships Autonomous Engine
Syncs upstream repo, searches listings, prioritizes target roles, and manages application queues.
"""

import sys
import os
import json
import subprocess
import webbrowser
from pathlib import Path

REPO_DIR = Path(r"e:\anti\Summer2027-Internships")
DATA_FILE = Path(r"e:\anti\data\summer2027_active.json")
TOP_FILE = Path(r"e:\anti\data\summer2027_top_targets.json")
DASHBOARD_FILE = Path(r"e:\anti\summer_2027_dashboard.html")

def sync_upstream():
    print("[+] Syncing upstream repository from SimplifyJobs/Summer2027-Internships...")
    if not REPO_DIR.exists():
        print(f"[-] Repository directory not found at {REPO_DIR}")
        return False

    cmd = ["git", "pull", "upstream", "dev"]
    res = subprocess.run(cmd, cwd=str(REPO_DIR), capture_output=True, text=True)
    print(res.stdout or res.stderr)

    print("[+] Re-processing listings data...")
    proc = subprocess.run([sys.executable, r"e:\anti\process_summer2027.py"], capture_output=True, text=True)
    print(proc.stdout)

    print("[+] Regenerating interactive dashboard...")
    gen = subprocess.run([sys.executable, r"e:\anti\generate_dashboard.py"], capture_output=True, text=True)
    print(gen.stdout)
    print("[✓] Sync completed successfully!")
    return True

def search_listings(query: str, limit: int = 15):
    if not DATA_FILE.exists():
        print("[-] Data file not found. Run sync first.")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    q = query.lower()
    matches = [
        j for j in jobs
        if q in j["company"].lower()
        or q in j["title"].lower()
        or q in j["category"].lower()
        or q in j["locations"].lower()
    ]

    print(f"\nFound {len(matches)} listings matching '{query}':")
    print("=" * 80)
    for i, j in enumerate(matches[:limit], 1):
        tier_tag = f"[{j['tier']}]" if j['tier'] != 'Enterprise / High Growth' else ""
        remote_tag = "[Remote]" if j['is_remote'] else ""
        print(f"{i:2d}. {j['company']} | {j['title']} {tier_tag} {remote_tag}")
        print(f"    Category: {j['category']} | Location: {j['locations']}")
        print(f"    Apply: {j['apply_url']}")
        if j.get("simplify_url"):
            print(f"    1-Click: {j['simplify_url']}")
        print("-" * 80)

def show_top(n: int = 15):
    if not TOP_FILE.exists():
        print("[-] Top targets file not found. Run processor first.")
        return

    with open(TOP_FILE, "r", encoding="utf-8") as f:
        targets = json.load(f)

    print(f"\nTop {min(n, len(targets))} Priority Target Opportunities for Summer 2027:")
    print("=" * 80)
    for i, j in enumerate(targets[:n], 1):
        print(f"{i:2d}. {j['company']} — {j['title']}")
        print(f"    Tier: {j['tier']} | Category: {j['category']} | Location: {j['locations']}")
        print(f"    Apply: {j['apply_url']}")
        print("-" * 80)

def open_dashboard():
    if DASHBOARD_FILE.exists():
        print(f"[+] Launching {DASHBOARD_FILE} in web browser...")
        webbrowser.open(DASHBOARD_FILE.as_uri())
    else:
        print("[-] Dashboard file not found.")

def main():
    if len(sys.argv) < 2:
        print("""Summer 2027 Internships Engine CLI
Usage:
  python summer_2027_engine.py --sync             # Pull latest updates from upstream and rebuild data/dashboard
  python summer_2027_engine.py --search <query>    # Search active listings by company/role/keyword
  python summer_2027_engine.py --top [N]           # Display top priority target opportunities
  python summer_2027_engine.py --dashboard         # Launch interactive browser dashboard
        """)
        return

    arg = sys.argv[1].lower()
    if arg in ["--sync", "-s", "sync"]:
        sync_upstream()
    elif arg in ["--search", "-q", "search"]:
        q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not q:
            print("Please provide a search term.")
            return
        search_listings(q)
    elif arg in ["--top", "-t", "top"]:
        n = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 15
        show_top(n)
    elif arg in ["--dashboard", "-d", "dashboard"]:
        open_dashboard()
    else:
        print(f"Unknown command: {arg}")

if __name__ == "__main__":
    main()
