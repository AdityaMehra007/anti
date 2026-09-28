#!/usr/bin/env python3
r"""
OMEGA BANGALORE EMAIL DISPATCH ACTIVATOR & LIVE SENDER
Helps the user configure their Gmail App Password and execute live automated dispatches.
"""

import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import smtplib
import time
from pathlib import Path
from email import message_from_bytes
from email.policy import default

ROOT_DIR = Path(r"E:\anti")
ENV_PATH = ROOT_DIR / ".env"
DISPATCH_SCRIPT = ROOT_DIR / "scripts" / "dispatch_all_bangalore_emails.py"
OUTBOX_TIER1 = ROOT_DIR / "applications_generated" / "corporate_eml_outbox"
OUTBOX_61 = ROOT_DIR / "Email_Drafts"

def print_banner():
    print("=" * 80)
    print("  OMEGA (INFINITY) BANGALORE LIVE EMAIL DISPATCH CONTROLLER")
    print("=" * 80)

def explain_gmail_setup():
    print("""
[!] NOTICE REGARDING AUTOMATED GMAIL ACCOUNT CREATION:
--------------------------------------------------------------------------------
Google enforces strict SMS phone verification and anti-bot CAPTCHAs that prevent
automated AI tools from creating fresh '@gmail.com' accounts programmatically.

HOWEVER, YOU HAVE TWO FAST, 100% WORKING OPTIONS:

================================================================================
OPTION A (RECOMMENDED: 60 SECONDS WITH YOUR EXISTING GMAIL)
================================================================================
Your verified email 'adityamehra799@gmail.com' is already built into all your 
resumes, cover letters, and application packages.

To allow this automated script to send emails through your Gmail:
  1. Open: https://myaccount.google.com/apppasswords
  2. Sign in to your Gmail (adityamehra799@gmail.com)
  3. App Name: Type "Antigravity Dispatcher" -> Click 'Create'
  4. Google will give you a 16-character code (e.g., 'abcd efgh ijkl mnop')
  5. Paste that 16-character code below!

================================================================================
OPTION B (CREATE A FRESH GMAIL MANUALLY IN 1 MINUTE)
================================================================================
  1. Open https://accounts.google.com/signup in your browser
  2. Create your new Gmail address (e.g., aditya.mehra.exec@gmail.com)
  3. Enable 2-Step Verification: https://myaccount.google.com/signinoptions/two-step-verification
  4. Create an App Password: https://myaccount.google.com/apppasswords
  5. Paste that email and 16-character code below!

================================================================================
OPTION C (ZERO SETUP: USE 1-CLICK WEB / DESKTOP MAILTO)
================================================================================
  If you don't want to use SMTP passwords, open:
  file:///E:/anti/apps/job_application_studio/bangalore_everything_master_hub.html
  Clicking 'Email HR Lead' opens your Gmail or Outlook with everything pre-filled!
================================================================================
""")

def test_and_save_credentials(user, app_password):
    print(f"\n[*] Testing connection to smtp.gmail.com:587 with {user}...")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.ehlo()
        server.starttls()
        server.login(user, app_password.replace(" ", ""))
        server.quit()
        print("[OK] SUCCESS! Gmail SMTP authenticated successfully.\n")
        
        # Save to .env
        env_lines = []
        if ENV_PATH.exists():
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                env_lines = f.readlines()
        
        # Filter out old gmail keys
        env_lines = [l for l in env_lines if not l.startswith("GMAIL_USER=") and not l.startswith("GMAIL_APP_PASSWORD=")]
        env_lines.append(f"GMAIL_USER={user}\n")
        env_lines.append(f"GMAIL_APP_PASSWORD={app_password.replace(' ', '')}\n")
        
        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.writelines(env_lines)
        print(f"[OK] Credentials saved securely to {ENV_PATH}")
        return True
    except Exception as e:
        print(f"[FAIL] Authentication failed: {e}")
        print("    Please verify that 2-Step Verification is enabled and you are using a 16-character App Password, NOT your normal Gmail login password.")
        return False

def dispatch_live_batch(user, app_password, limit=5):
    clean_pass = app_password.replace(" ", "")
    files = list(OUTBOX_61.glob("*.eml"))
    if not files:
        files = list(OUTBOX_TIER1.glob("*.eml"))
    
    selected_files = files[:limit]
    print(f"[*] Starting live dispatch of {len(selected_files)} premier applications...")
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(user, clean_pass)
    
    sent = 0
    for idx, fpath in enumerate(selected_files, 1):
        try:
            with open(fpath, "rb") as f:
                msg = message_from_bytes(f.read(), policy=default)
            to_addr = msg["To"]
            subject = msg["Subject"]
            print(f"[{idx}/{len(selected_files)}] Dispatching to: {to_addr} | Subj: {subject[:30]}...", end="", flush=True)
            server.send_message(msg)
            print(" -> [SENT OK]")
            sent += 1
            time.sleep(1.5)
        except Exception as e:
            print(f" -> [ERROR: {e}]")
    server.quit()
    print(f"\n[OK] Live dispatch run complete! Successfully sent {sent}/{len(selected_files)} applications.")

def main():
    print_banner()
    explain_gmail_setup()

    # Check if already present in env
    existing_user = os.getenv("GMAIL_USER")
    existing_pass = os.getenv("GMAIL_APP_PASSWORD")

    if not existing_user and ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("GMAIL_USER="):
                    existing_user = line.strip().split("=", 1)[1]
                elif line.startswith("GMAIL_APP_PASSWORD="):
                    existing_pass = line.strip().split("=", 1)[1]

    if existing_user and existing_pass:
        print(f"[i] Found configured account: {existing_user}")
        ans = input("Use this configured account? (y/n): ").strip().lower()
        if ans == "y":
            dispatch_live_batch(existing_user, existing_pass, limit=5)
            return

    user_input = input("Enter your Gmail address (e.g. adityamehra799@gmail.com): ").strip()
    if not user_input:
        print("No email provided. Exiting.")
        return
    
    pass_input = input("Enter your 16-character Google App Password: ").strip()
    if not pass_input:
        print("No App Password provided. Exiting.")
        return

    if test_and_save_credentials(user_input, pass_input):
        batch_str = input("How many emails would you like to dispatch right now? (default: 5): ").strip()
        batch_limit = int(batch_str) if batch_str.isdigit() else 5
        dispatch_live_batch(user_input, pass_input, limit=batch_limit)

if __name__ == "__main__":
    main()
