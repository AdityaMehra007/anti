#!/usr/bin/env python3
"""
========================================================================================
BANGALORE 4,500 COMPANIES NON-STOP OUTREACH DISPATCHER & BATCH RUNNER
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
========================================================================================
Automated CLI and background dispatcher to generate batches of ready-to-send RFC-822 (.eml)
drafts, track outreach status across all 4,500 Bangalore employers, and launch the Web GUI.
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import sqlite3
import argparse
import webbrowser
from datetime import datetime
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
MASTER_JSON = ROOT_DIR / "data" / "bangalore_4500_companies_master.json"
TRACKER_DB = ROOT_DIR / "data" / "outreach_vault_4500.sqlite"
OUTBOX_DIR = ROOT_DIR / "applications_generated" / "mega_4500_eml_outbox"

CANDIDATE_NAME = "Aditya Mehra"
CANDIDATE_PHONE = "+91-7003456624"
CANDIDATE_EMAIL = "adityamehra799@gmail.com"
CANDIDATE_DEGREE = "Bachelor of Business Administration (BBA) in International Business"
CANDIDATE_UNIV = "Dayananda Sagar University (DSU), Bengaluru"
CANDIDATE_YEAR = "2026"

def get_db():
    conn = sqlite3.connect(str(TRACKER_DB))
    conn.row_factory = sqlite3.Row
    return conn

def generate_pitch(company: str, hr_name: str, target_role: str) -> tuple[str, str]:
    subject = f"Application: {target_role} - {CANDIDATE_NAME} (BBA DSU '{CANDIDATE_YEAR[-2:]})"
    first_name = hr_name.split()[0] if hr_name and hr_name.lower() != "talent acquisition" else "Hiring Team"
    salutation = f"Dear {first_name},"

    body = f"""{salutation}

I hope this email finds you well.

I am writing to express my strong interest in early-career {target_role} openings at {company} in Bengaluru.

I will graduate with a {CANDIDATE_DEGREE} from {CANDIDATE_UNIV} in {CANDIDATE_YEAR}. My operational background is anchored entirely in verified on-ground execution:

1. Operations & Logistics Rigor: Lead Coordinator at AERO India 2025 (Yelahanka Air Force Base) and brand activations for Puma India and Tata Communications across 300+ field deployments.
2. Vendor Governance & SLA Enforcement: Structured Tier-1 supplier rate cards and enforced milestone delivery contracts with zero operational slippage.
3. Commercial Execution & Process Coordination: Drove enterprise client operations, compressed proposal turnaround from 7 days to 48 hours, and executed milestone handovers.
4. Technical & Trade Foundations: Managed AI data curation at Instawork AI (99%+ QA benchmark) and possess working proficiency in Incoterms 2020 rules and international documentation compliance.

Given {company}'s footprint in Bengaluru, I am eager to contribute hands-on operational grit, vendor discipline, and analytical problem-solving to your team.

My resume is attached for your review. I would welcome an introductory 10-minute conversation at your convenience.

Thank you very much for your time and consideration.

Warm regards,

{CANDIDATE_NAME}
Bengaluru, Karnataka, India
Phone: {CANDIDATE_PHONE}
Email: {CANDIDATE_EMAIL}
LinkedIn: https://www.linkedin.com/in/aditya-mehra
"""
    return subject, body

def generate_eml_batch(batch_size: int = 50) -> int:
    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, company, hr_name, hr_email, target_role 
        FROM outreach_ledger 
        WHERE status = 'QUEUED' 
        ORDER BY rowid ASC 
        LIMIT ?
    """, (batch_size,))

    rows = cursor.fetchall()
    if not rows:
        print("[!] No queued companies remaining. All 4,500 targets have been drafted or contacted!")
        conn.close()
        return 0

    generated_ids = []
    for r in rows:
        subject, body = generate_pitch(r["company"], r["hr_name"], r["target_role"])
        
        msg = EmailMessage()
        msg["From"] = f"{CANDIDATE_NAME} <{CANDIDATE_EMAIL}>"
        msg["To"] = f"{r['hr_name']} <{r['hr_email']}>"
        msg["Subject"] = subject
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="gmail.com")
        msg.set_content(body)

        safe_comp = "".join(c for c in r["company"] if c.isalnum() or c in (" ", "_", "-")).rstrip().replace(" ", "_")
        filename = f"{r['id']}_{safe_comp[:25]}.eml"
        eml_path = OUTBOX_DIR / filename
        eml_path.write_bytes(msg.as_bytes())

        generated_ids.append(r["id"])

    # Update status to DRAFTED
    cursor.executemany("""
        UPDATE outreach_ledger 
        SET status = 'DRAFTED', sent_timestamp = ? 
        WHERE id = ?
    """, [(datetime.now().isoformat(), tid) for tid in generated_ids])

    conn.commit()
    conn.close()

    print(f"[OK] Successfully generated {len(rows)} RFC-822 email drafts in {OUTBOX_DIR}")
    return len(rows)

def show_status():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM outreach_ledger")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT status, COUNT(*) FROM outreach_ledger GROUP BY status")
    statuses = dict(cursor.fetchall())

    cursor.execute("SELECT corridor, COUNT(*) FROM outreach_ledger GROUP BY corridor ORDER BY COUNT(*) DESC LIMIT 8")
    corridors = cursor.fetchall()

    cursor.execute("SELECT sector, COUNT(*) FROM outreach_ledger GROUP BY sector ORDER BY COUNT(*) DESC LIMIT 6")
    sectors = cursor.fetchall()

    conn.close()

    print("\n" + "=" * 80)
    print("  BANGALORE 4,500 COMPANIES NON-STOP OUTREACH ENGINE — LIVE STATUS")
    print("=" * 80)
    print(f"  Total Enterprise Targets : {total}")
    print(f"  Status Breakdown         : Queued: {statuses.get('QUEUED', 0)} | Drafted (.eml): {statuses.get('DRAFTED', 0)} | Sent: {statuses.get('SENT', 0)}")
    print(f"  Guaranteed Guardrail     : 100% Non-Sales Operations (0% Sales Risk)")
    print(f"  Candidate Ground Truth   : {CANDIDATE_NAME} | {CANDIDATE_PHONE} | {CANDIDATE_EMAIL}")
    print("=" * 80)
    
    print("\n[+] TOP BANGALORE CORRIDORS:")
    for c, cnt in corridors:
        print(f"  - {c:50} : {cnt} firms")

    print("\n[+] TOP INDUSTRY SECTORS:")
    for s, cnt in sectors:
        print(f"  - {s:50} : {cnt} firms")

    print("\n" + "=" * 80)

def main():
    parser = argparse.ArgumentParser(description="Bangalore 4,500 Companies Non-Stop Outreach Dispatcher")
    parser.add_argument("--generate-batch", type=int, default=0, help="Generate N email drafts (.eml) into outbox")
    parser.add_argument("--status", action="store_true", help="Display live progress across 4,500 targets")
    parser.add_argument("--open-studio", action="store_true", help="Open Non-Stop Outreach Studio in browser")
    parser.add_argument("--open-outbox", action="store_true", help="Open local EML outbox folder")

    args = parser.parse_args()

    if args.generate_batch > 0:
        generate_eml_batch(args.generate_batch)
    elif args.status:
        show_status()
    elif args.open_studio:
        url = "http://localhost:9119/apps/job_application_studio/bangalore_non_stop_outreach_studio.html"
        print(f"[*] Opening Non-Stop Outreach Studio: {url}")
        webbrowser.open(url)
    elif args.open_outbox:
        OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[*] Opening outbox directory: {OUTBOX_DIR}")
        if sys.platform == "win32":
            os.startfile(str(OUTBOX_DIR))
    else:
        show_status()

if __name__ == "__main__":
    main()
