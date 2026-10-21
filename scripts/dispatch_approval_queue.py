#!/usr/bin/env python3
"""
dispatch_approval_queue.py - Interactive Approval Queue & Dispatch Engine
==========================================================================
Enforces Section 5 (Mode F: Execution) & Section 27 (Human-in-the-Loop Governance).
Enables inspecting, approving, rejecting, and dispatching staged outreach actions
from data/approval_queue.csv into verified dispatch packets and audit ledgers.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import csv
import json
import urllib.parse
from pathlib import Path
from datetime import datetime
import argparse

ROOT_DIR = Path(r"e:\anti")
QUEUE_CSV = ROOT_DIR / "data" / "approval_queue.csv"
QUEUE_JSON = ROOT_DIR / "data" / "approval_queue.json"
DISPATCH_DIR = ROOT_DIR / "data" / "dispatched_actions"
AUDIT_LEDGER = ROOT_DIR / "data" / "dispatch_audit_ledger.jsonl"

def load_queue():
    if not QUEUE_CSV.exists():
        return []
    with open(QUEUE_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_queue(rows):
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    # Ensure Approved Timestamp and Dispatched Timestamp exist in header if present
    for extra in ["Approved Timestamp", "Dispatched Timestamp", "Dispatch Packet"]:
        if any(extra in r for r in rows) and extra not in fieldnames:
            fieldnames.append(extra)

    with open(QUEUE_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Sync to JSON
    with open(QUEUE_JSON, "w", encoding="utf-8") as f:
        json.dump({"updated_at": datetime.now().isoformat(), "total_actions": len(rows), "actions": rows}, f, indent=2)

def print_status_summary():
    rows = load_queue()
    if not rows:
        print("[!] approval_queue.csv is empty or missing.")
        return

    statuses = {}
    priorities = {}
    companies = {}

    for r in rows:
        st = r.get("Status", "UNKNOWN")
        pr = r.get("Priority", "UNKNOWN")
        cp = r.get("Company", "UNKNOWN")

        statuses[st] = statuses.get(st, 0) + 1
        priorities[pr] = priorities.get(pr, 0) + 1
        companies[cp] = companies.get(cp, 0) + 1

    print("=" * 65)
    print(f"📊 APPROVAL QUEUE STATUS SCORECARD — {len(rows)} Total Actions Staged")
    print("=" * 65)

    print("\n[Status Distribution]:")
    for s, c in sorted(statuses.items()):
        badge = "🟢" if s == "DISPATCHED" else ("🟡" if s == "APPROVED" else ("⚪" if s == "PENDING_APPROVAL" else "🔴"))
        print(f"  {badge} {s:<20}: {c:>4} actions ({c/len(rows)*100:>5.1f}%)")

    print("\n[Priority Distribution]:")
    for p, c in sorted(priorities.items()):
        print(f"  ⭐ {p:<22}: {c:>4} actions")

    top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\n[Top Target Companies]:")
    for comp, count in top_companies:
        print(f"  🏢 {comp:<24}: {count:>3} actions")

    pending = [r for r in rows if r.get("Status") == "PENDING_APPROVAL"]
    approved = [r for r in rows if r.get("Status") == "APPROVED"]
    dispatched = [r for r in rows if r.get("Status") == "DISPATCHED"]

    print("\n[Next Actions Ready]:")
    print(f"  • Pending Review: {len(pending)}")
    print(f"  • Approved Ready to Dispatch: {len(approved)}")
    print(f"  • Already Dispatched: {len(dispatched)}")
    print("=" * 65)

def approve_actions(action_ids=None, top_n=None, company=None):
    rows = load_queue()
    now_iso = datetime.now().isoformat()
    approved_count = 0

    target_ids = set([x.strip().upper() for x in action_ids.split(",")]) if action_ids else set()

    for r in rows:
        if r.get("Status") == "APPROVED":
            continue

        match = False
        if target_ids and r.get("Action ID", "").upper() in target_ids:
            match = True
        elif company and company.lower() in r.get("Company", "").lower():
            match = True
        elif top_n and approved_count < top_n and r.get("Status") == "PENDING_APPROVAL":
            match = True

        if match:
            r["Status"] = "APPROVED"
            r["Approved Timestamp"] = now_iso
            approved_count += 1

    save_queue(rows)
    print(f"✅ Approved {approved_count} action(s) in approval queue.")
    return approved_count

def reject_actions(action_ids):
    rows = load_queue()
    target_ids = set([x.strip().upper() for x in action_ids.split(",")])
    rejected_count = 0

    for r in rows:
        if r.get("Action ID", "").upper() in target_ids:
            r["Status"] = "REJECTED"
            rejected_count += 1

    save_queue(rows)
    print(f"🚫 Rejected {rejected_count} action(s).")
    return rejected_count

def dispatch_approved(limit=None):
    rows = load_queue()
    DISPATCH_DIR.mkdir(parents=True, exist_ok=True)
    now_iso = datetime.now().isoformat()

    approved_rows = [r for r in rows if r.get("Status") == "APPROVED"]
    if limit:
        approved_rows = approved_rows[:limit]

    if not approved_rows:
        print("[*] No actions currently in 'APPROVED' status. Run with --approve-top or approve specific IDs first.")
        return 0

    dispatched_count = 0
    ledger_entries = []

    for r in approved_rows:
        aid = r.get("Action ID", "ACT-UNKNOWN")
        company = r.get("Company", "Company")
        person = r.get("Person", "Recruiter")
        job = r.get("Job", "Role")
        channel = r.get("Channel", "LinkedIn / Direct")
        draft = r.get("Draft Message", "")
        reason = r.get("Reason / Evidence", "")

        # Format URL / Mailto / InMail Search
        safe_person = urllib.parse.quote(f"{person} {company}")
        linkedin_search_url = f"https://www.linkedin.com/search/results/people/?keywords={safe_person}"
        mailto_url = f"mailto:?subject={urllib.parse.quote(f'Application: {job} - Aditya Mehra')}&body={urllib.parse.quote(draft)}"

        safe_comp = "".join(c for c in company if c.isalnum() or c in ("_", "-")).strip()
        packet_filename = f"{aid}_{safe_comp}_dispatch_packet.md"
        packet_path = DISPATCH_DIR / packet_filename

        packet_content = f"""# DISPATCH PACKET — {aid}
**Status**: DISPATCHED  
**Dispatched At**: {now_iso}  
**Company**: {company}  
**Target Recruiter / Contact**: {person}  
**Job Opening**: {job}  
**Outreach Channel**: {channel}  
**Candidate**: Aditya Mehra (BBA 2026, Bangalore | adityamehra799@gmail.com)  

---

### VERIFIED EVIDENCE & MATCHING RATIONALE
{reason}

---

### DRAFT MESSAGE (Ready to Paste)
```text
{draft}
```

---

### 1-CLICK LAUNCH LINKS
- **LinkedIn Search Link**: [{person} at {company}]({linkedin_search_url})
- **Direct Mailto Client Link**: [Launch Email Client with Pre-filled Draft]({mailto_url})

---
*Generated by Antigravity Autonomous Dispatch Engine (OMEGA Constitution Directives 27-28)*
"""
        with open(packet_path, "w", encoding="utf-8") as f:
            f.write(packet_content)

        r["Status"] = "DISPATCHED"
        r["Dispatched Timestamp"] = now_iso
        try:
            r["Dispatch Packet"] = str(packet_path.relative_to(ROOT_DIR))
        except ValueError:
            r["Dispatch Packet"] = str(packet_path)
        dispatched_count += 1

        ledger_entries.append({
            "action_id": aid,
            "company": company,
            "person": person,
            "job": job,
            "channel": channel,
            "timestamp": now_iso,
            "packet_file": str(packet_path.name)
        })

    save_queue(rows)

    # Append to Audit Ledger
    with open(AUDIT_LEDGER, "a", encoding="utf-8") as f:
        for entry in ledger_entries:
            f.write(json.dumps(entry) + "\n")

    print(f"🚀 Successfully dispatched {dispatched_count} approved action(s)!")
    print(f"   Dispatch packets created in: {DISPATCH_DIR}")
    print(f"   Logged in audit ledger: {AUDIT_LEDGER}")
    return dispatched_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Approval Queue Management & Dispatch Gate")
    parser.add_argument("--status", action="store_true", help="Print summary scorecard of the approval queue")
    parser.add_argument("--approve", type=str, help="Comma-separated Action IDs to approve (e.g. ACT-0001,ACT-0002)")
    parser.add_argument("--approve-top", type=int, help="Approve top N pending actions")
    parser.add_argument("--approve-company", type=str, help="Approve all actions for a company (e.g. 'Accenture', 'TikTok')")
    parser.add_argument("--reject", type=str, help="Comma-separated Action IDs to reject")
    parser.add_argument("--dispatch", action="store_true", help="Dispatch all actions currently marked APPROVED")
    parser.add_argument("--dispatch-limit", type=int, default=None, help="Max number of approved actions to dispatch")
    parser.add_argument("--export-json", action="store_true", help="Export queue to data/approval_queue.json")
    args = parser.parse_args()

    if args.status:
        print_status_summary()
    elif args.approve:
        approve_actions(action_ids=args.approve)
    elif args.approve_top:
        approve_actions(top_n=args.approve_top)
    elif args.approve_company:
        approve_actions(company=args.approve_company)
    elif args.reject:
        reject_actions(args.reject)
    elif args.dispatch:
        dispatch_approved(limit=args.dispatch_limit)
    elif args.export_json:
        rows = load_queue()
        save_queue(rows)
        print(f"✅ Exported {len(rows)} actions to {QUEUE_JSON}")
    else:
        print_status_summary()
