import sqlite3
import urllib.parse
from pathlib import Path

def create_simple_fresher_email(company: str, contact_name: str):
    subject = f"Application: Entry-Level Roles / Operations - Aditya Mehra (BBA DSU Bengaluru | Immediate Joining)"
    
    body = f"""Hi {contact_name},

I hope you are doing well.

I recently completed my BBA in International Business from Dayananda Sagar University (DSU), Bengaluru (Class of 2026), and I am looking for entry-level opportunities at {company} across Operations, Operations Support, or Management Trainee roles. I am based in Bengaluru and available to join immediately.

A quick summary of my background:
• Corporate Internships: Worked on AI & robotics data collection at Instawork Services India (2025), and handled vendor tracking and client briefs in MS Excel at Pencil Mark Interior Solutions (2025).
• Field & Event Operations: Managed product sampling, customer handling, and live UPI billing at Aero India (Yelahanka) for chocolate brand Salt in My Cocoa, along with concert logistics.
• Family Business: Handled day-to-day order dispatches, billing, and Excel stock records in Kolkata (2018–2020).
• Tech & AI Tools: I actively use modern AI tools (Google Antigravity, Cursor, Python) to build small automation prototypes and save time on repetitive work (GitHub: github.com/AdityaMehra007/anti).

I am eager to learn, hardworking, and open to any suitable entry-level opening where I can contribute and grow.

I have attached my resume for your review. Please let me know if we can connect for a brief call.

Thank you for your time and consideration!

Best regards,

Aditya Mehra
Bengaluru, Karnataka
Phone: +91 7003456624
Email: adityamehra007@gmail.com
Portfolio: https://adi-digital-universe.ai.studio/
LinkedIn: linkedin.com/in/aditya-mehra-b8644b326
GitHub: github.com/AdityaMehra007
"""
    return subject, body

def update_all_emails():
    db_path = Path("data/outreach_tracker.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT application_id, company, contact_name, contact_email FROM automated_applications")
    rows = cur.fetchall()

    print(f"Updating all {len(rows)} emails to simple, friendly, high-conversion fresher format...")
    for app_id, company, contact_name, contact_email in rows:
        subject, body = create_simple_fresher_email(company, contact_name)
        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={urllib.parse.quote(contact_email)}&su={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        cur.execute("UPDATE automated_applications SET gmail_url = ? WHERE application_id = ?", (gmail_url, app_id))

    conn.commit()
    print("Database updated successfully!")

    # Also re-run grand universe generator to refresh the 1,500+ web portal
    from omega.orchestration.generate_grand_universe import generate_grand_universe_launcher
    generate_grand_universe_launcher()
    print("Web launcher refreshed with simple fresher emails!")

if __name__ == "__main__":
    update_all_emails()
