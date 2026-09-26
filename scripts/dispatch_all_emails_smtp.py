#!/usr/bin/env python3
"""
========================================================================================
AUTOMATED RECRUITER & AGENCY EMAIL DISPATCHER (SMTP)
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
========================================================================================
Safely dispatches pre-drafted .eml files from:
  1. applications_generated/agency_eml_outbox/ (15 Top Bangalore Headhunters)
  2. applications_generated/eml_outbox/ (150 Corporate Recruiters)

Modes:
  --dry-run   : Validates all .eml messages, recipients, and headers without sending.
  --agency    : Dispatches only the 15 Bangalore placement agencies.
  --corporate : Dispatches corporate recruiter emails.
  --send      : Actually sends via SMTP (requires GMAIL_USER and GMAIL_APP_PASSWORD env vars).
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import smtplib
import argparse
from pathlib import Path
from email import message_from_bytes
from email.policy import default

ROOT_DIR = Path(__file__).resolve().parent.parent
AGENCY_OUTBOX = ROOT_DIR / "applications_generated" / "agency_eml_outbox"
CORP_OUTBOX = ROOT_DIR / "applications_generated" / "eml_outbox"

def load_eml_files(folder: Path):
    if not folder.exists():
        return []
    return sorted(list(folder.glob("*.eml")))

def dispatch_emails(eml_files, dry_run=True, gmail_user=None, gmail_app_pass=None):
    print("=" * 80)
    print(f"  EMAIL DISPATCH CONTROLLER — Total Drafts: {len(eml_files)}")
    print(f"  Mode: {'DRY RUN (Validation only - no emails sent)' if dry_run else 'LIVE DISPATCH VIA SMTP'}")
    print("=" * 80)

    if not dry_run and (not gmail_user or not gmail_app_pass):
        print("[!] ERROR: Live dispatch requires GMAIL_USER and GMAIL_APP_PASSWORD.")
        print("    Set environment variables or pass --user and --pass arguments.")
        return 0

    server = None
    if not dry_run:
        try:
            print(f"[*] Connecting to smtp.gmail.com:587 as {gmail_user}...")
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_app_pass)
            print("[✓] SMTP Authentication Successful!")
        except Exception as e:
            print(f"[!] SMTP Connection failed: {e}")
            return 0

    sent_count = 0
    for idx, eml_path in enumerate(eml_files, 1):
        try:
            with open(eml_path, "rb") as f:
                msg = message_from_bytes(f.read(), policy=default)
            
            to_addr = msg["To"]
            subject = msg["Subject"]
            
            print(f"[{idx:03d}/{len(eml_files):03d}] To: {to_addr:<40} | Subj: {subject[:35]}...")
            
            if not dry_run and server:
                server.send_message(msg)
                sent_count += 1
            else:
                sent_count += 1
        except Exception as e:
            print(f"    [!] Failed processing {eml_path.name}: {e}")

    if server:
        server.quit()

    print("=" * 80)
    if dry_run:
        print(f"[✓] Validation complete: {sent_count}/{len(eml_files)} drafts verified and ready.")
    else:
        print(f"[✓] Live dispatch complete: {sent_count}/{len(eml_files)} emails sent successfully!")
    print("=" * 80)
    return sent_count

def main():
    parser = argparse.ArgumentParser(description="Automated Email Dispatcher")
    parser.add_argument("--agency", action="store_true", help="Process agency emails (15 drafts)")
    parser.add_argument("--corporate", action="store_true", help="Process corporate recruiter emails")
    parser.add_argument("--send", action="store_true", help="Actually send via SMTP (default is dry-run)")
    parser.add_argument("--user", type=str, default=os.getenv("GMAIL_USER"), help="Gmail address")
    parser.add_argument("--password", type=str, default=os.getenv("GMAIL_APP_PASSWORD"), help="Gmail 16-character App Password")

    args = parser.parse_args()

    files = []
    if args.agency or not args.corporate:
        files.extend(load_eml_files(AGENCY_OUTBOX))
    if args.corporate:
        files.extend(load_eml_files(CORP_OUTBOX))

    if not files:
        print("[!] No .eml files found in selected outboxes.")
        return

    dry_run = not args.send
    dispatch_emails(files, dry_run=dry_run, gmail_user=args.user, gmail_app_pass=args.password)

if __name__ == "__main__":
    main()
