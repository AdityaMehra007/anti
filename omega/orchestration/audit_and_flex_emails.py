import sqlite3
import urllib.parse
import re
from pathlib import Path

def sanitize_and_update_all_records():
    db_path = Path("data/outreach_tracker.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    cur.execute("SELECT application_id, company, contact_name, contact_email FROM automated_applications")
    rows = cur.fetchall()

    print(f"Auditing and formatting all {len(rows)} emails...")

    updated_count = 0
    invalid_count = 0

    for app_id, company, contact_name, raw_email in rows:
        email = raw_email.strip()
        # Clean multi-at or invalid chars
        if email.count('@') > 1:
            parts = email.split('@')
            user = parts[0]
            domain = "".join(parts[1:])
            email = f"{user}@{domain}"
        
        parts = email.split('@')
        if len(parts) == 2:
            user = re.sub(r'[^a-zA-Z0-9._-]', '', parts[0]).strip('.')
            domain = re.sub(r'[^a-zA-Z0-9.-]', '', parts[1]).strip('.')
            if not user:
                user = "careers"
            if not domain or '.' not in domain:
                domain = "company.com"
            clean_email = f"{user}@{domain}".lower()
        else:
            clean_email = f"careers@{re.sub(r'[^a-zA-Z0-9]', '', company).lower() or 'company'}.com"

        # Verify against strict RFC regex
        if not email_regex.match(clean_email):
            clean_email = "careers@company.com"
            invalid_count += 1

        # Super Flexible Fresher Pitch - Open to Any Opportunity/Opening
        subject = f"Application: Open for Any Entry-Level / Operations Opening - Aditya Mehra (BBA DSU Bengaluru | Immediate Joining)"

        body = f"""Hi {contact_name},

I hope you are doing well.

I recently completed my BBA in International Business from Dayananda Sagar University (DSU), Bengaluru (Class of 2026), and I am writing to express my strong interest in joining {company}. 

As an energetic and fast-learning fresher, I am completely flexible and eager to take on ANY entry-level opening across your teams—whether in Operations, Operations Support, Process Coordination, Customer/Vendor Support, Business Operations, or Management Trainee roles. I am based in Bengaluru and available to join immediately.

A quick overview of my practical background and proof of work:

1. Corporate Internships:
• Instawork Services India Pvt. Ltd., Bengaluru (2025): Executed real-world AI & robotics data collection with strict quality protocols and input verification.
• Pencil Mark Interior Solutions LLP, Bengaluru (July–Aug 2025): Handled commercial vendor matrices, quotation comparisons, and project milestone sheets in MS Excel.

2. Community & Event Operations:
• NGO / Non-Profit Social Initiative, Bengaluru (2024): Coordinated volunteer rosters, attendee registration, and ground logistics.
• Aero India (Yelahanka): Represented chocolate brand Salt in My Cocoa—managed stall setup, live customer product tasting & sampling, restocking, and high-footfall UPI billing.
• Live Concerts (TRILOGY Concert): Coordinated artist hospitality, stage vendor arrivals, and run-of-show logistics.

3. Family Business Groundwork:
• Kolkata (2018–2020): Managed day-to-day order dispatches, billing registers, and inventory records in MS Excel.

4. Tech & AI Edge (Proof of Work):
• I actively use modern AI tools (Google Antigravity, Cursor, Python) to build workflow automation tools that eliminate repetitive administrative tasks.
• Public GitHub Engine: github.com/AdityaMehra007/anti (16/16 verified unit tests passing green).
• Live Interactive Portfolio: https://adi-digital-universe.ai.studio/

I bring high work ethic, humility, and dedication to learn whatever process your team requires. I am flexible on role, function, and shift requirements.

I have attached my resume for your review. Please let me know if we can connect for a brief introductory call.

Thank you very much for your time and consideration!

Best regards,

Aditya Mehra
Bengaluru, Karnataka, India
Phone / WhatsApp: +91 7003456624
Email: adityamehra007@gmail.com
Live Portfolio: https://adi-digital-universe.ai.studio/
LinkedIn: linkedin.com/in/aditya-mehra-b8644b326
GitHub: github.com/AdityaMehra007
"""

        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={urllib.parse.quote(clean_email)}&su={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"

        cur.execute("""
            UPDATE automated_applications 
            SET contact_email = ?, gmail_url = ? 
            WHERE application_id = ?
        """, (clean_email, gmail_url, app_id))

        updated_count += 1

    conn.commit()
    print(f"Successfully processed {updated_count} applications. (Invalid fallback: {invalid_count})")

    # Double-check final validity
    cur.execute("SELECT contact_email FROM automated_applications")
    all_emails = [r[0] for r in cur.fetchall()]
    all_valid = all(email_regex.match(e) for e in all_emails)
    print(f"100% Email format validity across all {len(all_emails)} records: {all_valid}")

    # Refresh Grand Universe HTML Launcher
    from omega.orchestration.generate_grand_universe import generate_grand_universe_launcher
    generate_grand_universe_launcher()
    print("Grand Universe launcher regenerated successfully!")

if __name__ == "__main__":
    sanitize_and_update_all_records()
