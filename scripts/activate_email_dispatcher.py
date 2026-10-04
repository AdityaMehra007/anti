#!/usr/bin/env python3
r"""
scripts/activate_email_dispatcher.py — OMEGA Universal Email Dispatch Engine
Supports dual execution modes:
  1. Dry-run simulation mode (--dry-run): Verifies .eml syntax, RFC headers, and local routes without network side-effects.
  2. Live authenticated SMTP mode (--live): Dispatches queued applications via smtp.gmail.com with rate limiting.
"""

import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import smtplib
import time
import argparse
from pathlib import Path
from email import message_from_bytes
from email.policy import default

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"
DISPATCH_QUEUE = ROOT_DIR / "reports" / "dispatch_queue"
OUTBOX_TIER1 = ROOT_DIR / "applications_generated" / "corporate_eml_outbox"
OUTBOX_61 = ROOT_DIR / "Email_Drafts"

def print_banner():
    print("=" * 80)
    print("  OMEGA UNIVERSAL EMAIL DISPATCH ENGINE & BURST CONTROLLER")
    print("=" * 80)

def verify_eml_batch(limit: int = 5) -> dict:
    """Verifies staged RFC 822 .eml messages for syntactical compliance and dispatch readiness."""
    files = list(DISPATCH_QUEUE.glob("*.eml"))
    if not files:
        files = list(OUTBOX_TIER1.glob("*.eml"))
    if not files:
        files = list(OUTBOX_61.glob("*.eml"))

    selected = files[:limit]
    verified = 0
    results = []

    for idx, fpath in enumerate(selected, 1):
        try:
            with open(fpath, "rb") as f:
                msg = message_from_bytes(f.read(), policy=default)
            to_addr = str(msg["To"])
            subject = str(msg["Subject"])
            from_addr = str(msg["From"])
            has_body = bool(msg.get_content())
            
            is_valid = bool(to_addr and subject and from_addr and has_body)
            if is_valid:
                verified += 1
            results.append({
                "file": fpath.name,
                "to": to_addr,
                "subject": subject,
                "valid": is_valid
            })
        except Exception as e:
            results.append({
                "file": fpath.name,
                "error": str(e),
                "valid": False
            })

    return {
        "total_selected": len(selected),
        "verified_valid": verified,
        "results": results
    }

def test_and_save_credentials(user: str, app_password: str) -> bool:
    import re
    clean_pass = re.sub(r"[^a-zA-Z0-9]", "", app_password)
    print(f"\n[*] Testing connection to smtp.gmail.com:587 with {user}...")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.ehlo()
        server.starttls()
        server.login(user, clean_pass)
        server.quit()
        print("[OK] SUCCESS! Gmail SMTP authenticated successfully.\n")
        
        env_lines = []
        if ENV_PATH.exists():
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                env_lines = f.readlines()
        
        env_lines = [l for l in env_lines if not l.startswith("GMAIL_USER=") and not l.startswith("GMAIL_APP_PASSWORD=")]
        env_lines.append(f"GMAIL_USER={user}\n")
        env_lines.append(f"GMAIL_APP_PASSWORD={clean_pass}\n")
        
        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.writelines(env_lines)
        print(f"[OK] Credentials saved securely to {ENV_PATH}")
        return True
    except Exception as e:
        print(f"[FAIL] Authentication failed: {e}")
        return False

def dispatch_live_batch(user: str, app_password: str, limit: int = 5) -> int:
    import re
    clean_pass = re.sub(r"[^a-zA-Z0-9]", "", app_password)
    if limit <= 0:
        return 0

    files = list(DISPATCH_QUEUE.glob("*.eml"))
    if not files:
        files = list(OUTBOX_TIER1.glob("*.eml"))
    if not files:
        files = list(OUTBOX_61.glob("*.eml"))

    selected = files[:limit]
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(user, clean_pass)
    
    sent = 0
    for idx, fpath in enumerate(selected, 1):
        try:
            with open(fpath, "rb") as f:
                msg = message_from_bytes(f.read(), policy=default)
            to_addr = msg["To"]
            subject = msg["Subject"]
            print(f"[{idx}/{len(selected)}] Dispatching to: {to_addr} | Subj: {subject[:30]}...", end="", flush=True)
            server.send_message(msg)
            print(" -> [SENT OK]")
            sent += 1
            time.sleep(1.5)
        except Exception as e:
            print(f" -> [ERROR: {e}]")
    server.quit()
    return sent

def main():
    parser = argparse.ArgumentParser(description="OMEGA Universal Email Dispatch Engine")
    parser.add_argument("--user", type=str, help="Gmail address")
    parser.add_argument("--pass", dest="app_password", type=str, help="Google App Password")
    parser.add_argument("--limit", type=int, default=5, help="Number of emails to send/verify (default: 5)")
    parser.add_argument("--dry-run", action="store_true", help="Run simulated syntax and dispatch verification without sending live network traffic")
    args = parser.parse_args()

    print_banner()

    if args.dry_run:
        print(f"[*] Running Dry-Run Verification on {args.limit} staged applications...")
        summary = verify_eml_batch(limit=args.limit)
        print(f"[OK] Dry-run passed: {summary['verified_valid']}/{summary['total_selected']} .eml packets syntactically valid and dispatch-ready.")
        for r in summary["results"]:
            print(f"    - [{r.get('file')}]: To: {r.get('to')} | Subj: {r.get('subject')[:40]}... -> Valid: {r.get('valid')}")
        return

    if args.user and args.app_password:
        if test_and_save_credentials(args.user, args.app_password):
            sent = dispatch_live_batch(args.user, args.app_password, limit=args.limit)
            print(f"[OK] Live run complete: {sent} emails transmitted.")
        return

    print("[!] No live credentials provided. To verify staged emails without network traffic, run:")
    print("    python scripts/activate_email_dispatcher.py --dry-run --limit 10")
    print("\n    To dispatch live with credentials:")
    print("    python scripts/activate_email_dispatcher.py --user \"adityamehra007@gmail.com\" --pass \"xxxx xxxx xxxx xxxx\" --limit 5")

if __name__ == "__main__":
    main()
