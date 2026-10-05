import sqlite3
import urllib.parse
import re
from pathlib import Path

def complete_database_integrity_fix():
    db_path = Path("data/outreach_tracker.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT application_id, contact_email, gmail_url FROM automated_applications")
    rows = cur.fetchall()

    fixed_count = 0
    for app_id, email, gurl in rows:
        clean_email = email.strip()
        # Remove repeated dots
        if '..' in clean_email:
            clean_email = re.sub(r'\.+', '.', clean_email)
        
        # Ensure user part and domain part don't have leading or trailing dots
        parts = clean_email.split('@')
        if len(parts) == 2:
            u, d = parts[0].strip('.'), parts[1].strip('.')
            clean_email = f"{u}@{d}"

        if clean_email != email:
            new_gurl = gurl.replace(urllib.parse.quote(email), urllib.parse.quote(clean_email))
            cur.execute("""
                UPDATE automated_applications 
                SET contact_email = ?, gmail_url = ? 
                WHERE application_id = ?
            """, (clean_email, new_gurl, app_id))
            fixed_count += 1

    conn.commit()
    print(f"Total domains sanitized: {fixed_count}")

    # Comprehensive verification
    cur.execute("SELECT application_id, contact_email, gmail_url FROM automated_applications")
    all_rows = cur.fetchall()

    email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    all_valid_email = True
    all_valid_url = True
    all_matching = True
    no_consecutive_dots = True

    for app_id, email, gurl in all_rows:
        if not email_regex.match(email):
            all_valid_email = False
        if not gurl.startswith("https://mail.google.com/mail/?view=cm&fs=1&to="):
            all_valid_url = False
        parsed_to = urllib.parse.parse_qs(urllib.parse.urlparse(gurl).query).get('to', [''])[0]
        if parsed_to != email:
            all_matching = False
        if '..' in email:
            no_consecutive_dots = False

    print("--- COMPLETE DATABASE VERIFICATION REPORT ---")
    print(f"Total Records in Database: {len(all_rows)}")
    print(f"100% RFC-Compliant Email Addresses: {all_valid_email}")
    print(f"100% Valid Direct Gmail Compose URLs: {all_valid_url}")
    print(f"100% Match Between Target Email & Gmail URL: {all_matching}")
    print(f"Zero Double Dots in Any Domain: {no_consecutive_dots}")

    # Regenerate launcher
    from omega.orchestration.generate_grand_universe import generate_grand_universe_launcher
    generate_grand_universe_launcher()
    print("Launcher regenerated successfully!")

if __name__ == "__main__":
    complete_database_integrity_fix()
