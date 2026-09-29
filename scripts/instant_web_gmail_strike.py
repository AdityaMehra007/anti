#!/usr/bin/env python3
r"""
INSTANT WEB GMAIL STRIKE ENGINE (ZERO-PASSWORD REQUIRED)
Bypasses SMTP authentication by launching direct Gmail Web Compose URLs
in your active browser session with recipient, subject, and tailored pitch pre-filled.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import json
import sqlite3
import webbrowser
import time
from urllib.parse import quote
from pathlib import Path

ROOT_DIR = Path(r"E:\anti")
TARGETS_JSON = ROOT_DIR / "data" / "BANGALORE_MEGA_4500_TARGETS.json"
VAULT_DB = ROOT_DIR / "data" / "outreach_vault_4500.sqlite"
CORE_DB = ROOT_DIR / "data" / "aditya_global_career_intelligence.db"

def main(start=0, limit=5):
    print("=" * 80)
    print("  OMEGA INSTANT WEB GMAIL STRIKE ENGINE — ZERO-PASSWORD DIRECT LAUNCH")
    print("=" * 80)

    with open(TARGETS_JSON, "r", encoding="utf-8") as f:
        targets = json.load(f)

    # Pick batch
    selected = targets[start:start+limit]

    print(f"[*] Preparing {len(selected)} high-conviction Bangalore applications (Offset: {start})...")

    conn_vault = sqlite3.connect(VAULT_DB)
    cur_vault = conn_vault.cursor()

    launched_urls = []

    for idx, t in enumerate(selected, start + 1):
        company = t.get("company", "Bangalore Tech Corp")
        hr_name = t.get("hr_name", "Talent Acquisition Lead")
        to_email = t.get("hr_email") or t.get("careers_email") or "careers@company.com"
        subject = t.get("email_subject") or f"Application: Operations & Business Execution Analyst - Aditya Mehra (BBA DSU '26)"
        body = t.get("email_body") or f"Dear {hr_name},\n\nPlease find attached my resume for operations opportunities at {company}."

        # Gmail Web Compose URL format:
        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={quote(to_email)}&su={quote(subject)}&body={quote(body)}"
        launched_urls.append((company, hr_name, to_email, gmail_url))

        # Update vault status
        cur_vault.execute("UPDATE outreach_ledger SET status = 'STRIKE_LAUNCHED' WHERE id = ?", (t.get("id"),))

        print(f"\n[{idx}] STRIKE TARGET: {company}")
        print(f"   HR Contact: {hr_name} <{to_email}>")
        print(f"   Subject:    {subject}")
        print(f"   Action:     Launching Web Gmail Compose Tab...")

        # Open in default browser
        webbrowser.open(gmail_url)
        time.sleep(1.0)

    conn_vault.commit()
    conn_vault.close()

    print("\n" + "=" * 80)
    print("  [OK] ALL TABS LAUNCHED DIRECTLY IN YOUR BROWSER!")
    print("  Check your browser window — each email is pre-filled and ready to send.")
    print("=" * 80)

if __name__ == "__main__":
    start = 0
    count = 5
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        count = int(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2].isdigit():
        start = int(sys.argv[2])
    main(start=start, limit=count)
