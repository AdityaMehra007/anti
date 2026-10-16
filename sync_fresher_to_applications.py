#!/usr/bin/env python3
import csv
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

workspace = Path(r"e:\anti")
app_file = workspace / "job_applications.csv"
live_file = workspace / "BANGALORE_ZERO_EXP_FRESHERS_LIVE.csv"

with open(app_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    app_headers = next(reader)
    app_rows = list(reader)

existing_keys = set()
for r in app_rows:
    if len(r) >= 3:
        existing_keys.add((r[1].strip().lower(), r[2].strip().lower()))

print(f"Existing job_applications.csv count: {len(app_rows)}")

with open(live_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    live_entries = list(reader)

new_added = 0
for entry in live_entries:
    comp = entry["Company"].strip()
    role = entry["Role & Track"].strip()
    key = (comp.lower(), role.lower())
    if key not in existing_keys:
        notes = f"Job ID: {entry.get('Job Requisition ID', 'N/A')}. CTC: {entry.get('CTC Bracket', 'Market')}. JD Fit: {entry.get('JD Fit Analysis', '100% Fit')}"
        row = [
            "2026-10-13",
            comp,
            role,
            f"Bengaluru ({entry['Cluster / Tech Park']})",
            entry["Category"],
            entry["Portal URL"],
            "READY_TO_APPLY",
            "2026-10-16",
            entry["Internal Referral Contact"],
            notes
        ]
        app_rows.append(row)
        existing_keys.add(key)
        new_added += 1

print(f"New roles added: {new_added}")
print(f"Total job_applications.csv count now: {len(app_rows)}")

with open(app_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(app_headers)
    writer.writerows(app_rows)

print("Successfully synchronized job_applications.csv")
