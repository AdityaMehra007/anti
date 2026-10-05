import sqlite3
import urllib.parse
from pathlib import Path

def create_complete_email(company: str, contact_name: str):
    subject = f"Application: Entry-Level Roles / Operations - Aditya Mehra (BBA DSU Bengaluru | Immediate Joining)"
    
    body = f"""Hi {contact_name},

I hope you are doing well.

I recently completed my BBA in International Business from Dayananda Sagar University (DSU), Bengaluru (Class of 2026), and I am writing to apply for entry-level opportunities at {company} across Operations, Operations Support, or Management Trainee roles. I am based in Bengaluru and available to join immediately.

Here is a complete summary of my practical background and proof of work:

1. Corporate Internships (2 Real Corporate Roles):
• Instawork Services India Pvt. Ltd., Bengaluru (2025): Executed real-world AI & robotics data collection adhering to strict quality protocols, verified input accuracy, and operational benchmarks.
• Pencil Mark Interior Solutions LLP, Bengaluru (July–Aug 2025): Translated commercial client requirements into project briefs; maintained vendor quotation matrices, cost comparisons, and delivery milestone trackers in MS Excel.

2. Community & NGO Work:
• NGO / Non-Profit Social Initiative, Bengaluru (2024): Coordinated volunteer shift rosters, attendee registration, and on-ground logistics for social awareness drives.

3. Field Operations & Brand Activations:
• Aero India (Air Force Station Yelahanka): Represented artisan chocolate brand Salt in My Cocoa—managed booth setup, live customer tasting & product sampling, inventory stock replenishments, and high-footfall UPI transactions.
• Live Concerts & Entertainment: Coordinated artist hospitality, stage vendor arrivals, and run-of-show logistics (TRILOGY Concert).

4. Family Business Experience:
• Kolkata (2018–2020): Managed customer billing, supplier dispatches, and daily stock movement ledgers in MS Excel.

5. Modern Tech Edge & AI Prototyping (Proof of Work):
• Unlike traditional business graduates, I use modern AI tools (Google Antigravity, Cursor, Python) to build automation prototypes that eliminate repetitive administrative work.
• Public GitHub Engine: github.com/AdityaMehra007/anti (Autonomous operations engine with 16/16 verified unit tests).
• Live Interactive Portfolio: https://adi-digital-universe.ai.studio/

I am a quick learner, dependable, and open to any suitable entry-level opening where I can contribute with high work ethic and grow.

I have attached my resume for your review. Please let me know if we can connect for a brief call.

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
    return subject, body

def update_all_emails():
    db_path = Path("data/outreach_tracker.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT application_id, company, contact_name, contact_email FROM automated_applications")
    rows = cur.fetchall()

    print(f"Updating all {len(rows)} application emails with complete comprehensive proof-of-work pitch...")
    for app_id, company, contact_name, contact_email in rows:
        subject, body = create_complete_email(company, contact_name)
        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={urllib.parse.quote(contact_email)}&su={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        cur.execute("UPDATE automated_applications SET gmail_url = ? WHERE application_id = ?", (gmail_url, app_id))

    conn.commit()
    print("Database updated successfully!")

    from omega.orchestration.generate_grand_universe import generate_grand_universe_launcher
    generate_grand_universe_launcher()
    print("Grand Universe web launcher regenerated with complete email pitches!")

if __name__ == "__main__":
    update_all_emails()
