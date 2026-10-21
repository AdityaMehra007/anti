#!/usr/bin/env python3
"""
sync_cockpit_queue.py - Synchronizes Approval Queue Data into Static Cockpit HTML
==================================================================================
Ensures both local file:// opening and live HTTP serving reflect exact queue states:
- CSV -> JSON synchronization
- Injects updated JSON into universal_job_cockpit.html
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "approval_queue.csv"
JSON_PATH = ROOT / "data" / "approval_queue.json"
HTML_PATH = ROOT / "universal_job_cockpit.html"

def sync():
    if not CSV_PATH.exists():
        print(f"❌ {CSV_PATH} not found.")
        return False

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    from datetime import datetime
    # Write JSON
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": datetime.now().isoformat(),
            "total_actions": len(rows),
            "actions": rows
        }, f, indent=2)
    print(f"✅ Synchronized {len(rows)} records to {JSON_PATH}")

    # Inject into HTML safely without regex escape bugs
    if HTML_PATH.exists():
        html = HTML_PATH.read_text(encoding="utf-8")
        json_str = json.dumps(rows)
        target_prefix = "let queueActions = ["
        idx_start = html.find(target_prefix)
        if idx_start != -1:
            idx_end = html.find("];", idx_start)
            if idx_end != -1:
                new_html = html[:idx_start] + f"let queueActions = {json_str}" + html[idx_end:]
                HTML_PATH.write_text(new_html, encoding="utf-8")
                print(f"✅ Injected updated queueActions into {HTML_PATH}")
            else:
                print("⚠️ Closing bracket for queueActions not found in HTML.")
        else:
            print("⚠️ Target prefix 'let queueActions = [' not found in HTML.")

    dispatched = sum(1 for r in rows if r.get("Status") == "DISPATCHED")
    approved = sum(1 for r in rows if r.get("Status") == "APPROVED")
    pending = sum(1 for r in rows if r.get("Status") == "PENDING_APPROVAL")
    print(f"📊 Queue State: {len(rows)} Total | {dispatched} Dispatched | {approved} Approved | {pending} Pending")
    return True

if __name__ == "__main__":
    sync()
