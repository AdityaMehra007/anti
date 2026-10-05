import sqlite3
import urllib.parse
import re
from pathlib import Path

def update_all_emails_with_live_resume_attachment():
    db_path = Path("data/outreach_tracker.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    cur.execute("SELECT application_id, company, contact_name, contact_email FROM automated_applications")
    rows = cur.fetchall()

    print(f"Updating all {len(rows)} emails to include live verified resume links and flexible pitch...")

    for app_id, company, contact_name, clean_email in rows:
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
• Public GitHub Engine: https://github.com/AdityaMehra007/anti (16/16 verified unit tests passing green).
• Live Interactive Portfolio: https://adi-digital-universe.ai.studio/

📄 Direct Resume Links (Attached & Online):
• Verified Word Resume (.DOCX): https://raw.githubusercontent.com/AdityaMehra007/anti/master/resumes/Aditya_Mehra_Resume_Master_Operations_2026.docx
• Clean Web Resume (.MD): https://raw.githubusercontent.com/AdityaMehra007/anti/master/resume_adi.md

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
GitHub: https://github.com/AdityaMehra007
"""

        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={urllib.parse.quote(clean_email)}&su={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"

        cur.execute("""
            UPDATE automated_applications 
            SET gmail_url = ? 
            WHERE application_id = ?
        """, (gmail_url, app_id))

    conn.commit()
    print("Database updated with live resume links!")

    # Update generator to also have one-click resume download / copy path
    from omega.orchestration.generate_grand_universe import generate_grand_universe_launcher
    generate_grand_universe_launcher()
    print("Grand Universe launcher regenerated successfully!")

if __name__ == "__main__":
    update_all_emails_with_live_resume_attachment()
