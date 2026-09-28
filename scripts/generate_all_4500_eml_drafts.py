#!/usr/bin/env python3
r"""
OMEGA 4,500 EML OUTBOX GENERATOR
Generates all 4,500 RFC-822 .eml draft files on disk into:
E:\anti\applications_generated\mega_4500_eml_outbox\
And updates outreach_vault_4500.sqlite status to 'DRAFTED'.
"""

import os
import sys
import json
import re
import sqlite3
from pathlib import Path
from email.message import EmailMessage
from email.utils import make_msgid, formatdate

ROOT_DIR = Path(r"E:\anti")
TARGETS_JSON = ROOT_DIR / "data" / "BANGALORE_MEGA_4500_TARGETS.json"
OUTBOX_DIR = ROOT_DIR / "applications_generated" / "mega_4500_eml_outbox"
DB_PATH = ROOT_DIR / "data" / "outreach_vault_4500.sqlite"

CANDIDATE_NAME = "Aditya Mehra"
CANDIDATE_EMAIL = "adityamehra799@gmail.com"

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "_", text)

def main():
    print("=" * 80)
    print("  OMEGA 4,500 ALL-BANGALORE EML OUTBOX COMPILER")
    print("=" * 80)

    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[*] Loading targets from {TARGETS_JSON}...")
    with open(TARGETS_JSON, "r", encoding="utf-8") as f:
        targets = json.load(f)
    print(f"[+] Loaded {len(targets):,} targets.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    existing_files = set(f.name for f in OUTBOX_DIR.glob("*.eml"))
    print(f"[*] Found {len(existing_files):,} existing .eml files. Generating remainder...")

    generated = 0
    updated_ids = []

    for t in targets:
        tid = t.get("id", f"HR-BLR-{t.get('index', 0):04d}")
        company = t.get("company", "Bangalore Enterprise")
        clean_comp = slugify(company)[:30]
        fname = f"{tid}_{clean_comp}.eml"

        to_name = t.get("hr_name", "Talent Acquisition Lead")
        to_email = t.get("hr_email") or t.get("careers_email") or "careers@company.com"
        subject = t.get("email_subject") or f"Application: {t.get('job_title', 'Business Operations Analyst')} - Aditya Mehra (BBA DSU '26)"
        body = t.get("email_body") or "Dear Hiring Team,\n\nPlease review my attached resume for early-career operations openings.\n\nWarm regards,\nAditya Mehra"

        fpath = OUTBOX_DIR / fname

        if fname not in existing_files:
            msg = EmailMessage()
            msg["From"] = f"{CANDIDATE_NAME} <{CANDIDATE_EMAIL}>"
            msg["To"] = f"{to_name} <{to_email}>"
            msg["Subject"] = subject
            msg["Date"] = formatdate(localtime=True)
            msg["Message-ID"] = make_msgid(domain="gmail.com")
            msg.set_content(body)

            with open(fpath, "wb") as out_file:
                out_file.write(msg.as_bytes())
            generated += 1

        updated_ids.append(tid)

    # Update SQLite database to mark them as DRAFTED
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outreach_ledger (
            id TEXT PRIMARY KEY,
            company TEXT NOT NULL,
            hr_name TEXT,
            hr_email TEXT NOT NULL,
            phone TEXT,
            corridor TEXT,
            sector TEXT,
            target_role TEXT,
            status TEXT DEFAULT 'QUEUED',
            sent_timestamp DATETIME,
            response_status TEXT DEFAULT 'NONE',
            notes TEXT
        )
    """)
    cursor.execute("UPDATE outreach_ledger SET status = 'DRAFTED' WHERE status != 'SENT'")
    conn.commit()
    conn.close()

    total_emls = len(list(OUTBOX_DIR.glob("*.eml")))
    print("=" * 80)
    print(f"[OK] COMPILATION COMPLETE!")
    print(f"  * Newly Generated: {generated:,} .eml files")
    print(f"  * Total EML Drafts on Disk: {total_emls:,} in {OUTBOX_DIR}")
    print(f"  * SQLite Ledger Updated: {len(updated_ids):,} records marked DRAFTED")
    print("=" * 80)

if __name__ == "__main__":
    main()
