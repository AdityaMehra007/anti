#!/usr/bin/env python3
import csv
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

workspace = Path(r"e:\anti")
live_file = workspace / "BANGALORE_ZERO_EXP_FRESHERS_LIVE.csv"
board_file = workspace / "ACTIVE_HIRING_MNC_STRIKE_BOARD.md"

with open(live_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    live_jobs = list(reader)

with open(board_file, "r", encoding="utf-8") as f:
    content = f.read()

added = 0
new_lines = []
for i, j in enumerate(live_jobs):
    comp = j["Company"]
    role = j["Role & Track"]
    if comp not in content or role not in content:
        job_id = j.get("Job Requisition ID") or f"BLR-FRESHER-{i+1:02d}"
        portal_url = j["Portal URL"]
        link = f"[Apply on Portal]({portal_url})"
        contact = j.get("Internal Referral Contact", "Talent Acquisition Team")
        row = f"| `{job_id}` | **{comp}** | {role} | **Live 0-Exp** | {link} | {contact} |"
        new_lines.append(row)
        added += 1

print(f"Roles to add to strike board: {added}")
if new_lines:
    updated = content.rstrip() + "\n" + "\n".join(new_lines) + "\n"
    with open(board_file, "w", encoding="utf-8") as f:
        f.write(updated)
    print(f"Successfully synced {added} roles into ACTIVE_HIRING_MNC_STRIKE_BOARD.md")
else:
    print("All roles already present on the strike board.")
