"""
DISPATCH_APPROVED_STRIKES.py - OMEGA Autonomous Outreach & Application Staging Dispatcher
========================================================================================
Parses the verified approval queue and outputs copy-paste ready, high-converting recruiter 
outreach packets linking to the live portfolio showcase and passing test suites.
"""

import csv
import json
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(r"e:\anti")
APPROVAL_CSV = ROOT_DIR / "data" / "approval_queue.csv"
OUTPUT_DIR = ROOT_DIR / "applications_generated" / "outreach_strikes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HIGH_CONVERTING_TEMPLATE = """Subject: Application: {title} — Aditya Mehra (DSU BBA '26 • Immediate Joiner)

Dear {first_name},

I am writing directly to express my high-conviction interest in the {title} role at {company}. As an International Business graduate (Dayananda Sagar University, Bengaluru) with immediate joining availability, I combine real-world ground operations with high-concurrency systems engineering:

• High-Concurrency Systems Engineering: Architected ApexFlow, an asynchronous 3-way reconciliation engine processing 56,179 transactions/sec at sub-18 microsecond latency with cryptographic SHA-256 idempotency and self-healing circuit breakers to eliminate enterprise procurement leakage.
• High-Stakes Ground Operations: Led exhibition logistics for 100,000+ defense & commercial visitors at AERO INDIA 2025 (Yelahanka Air Force Station) enforcing 0.0% inventory shrinkage and 100% on-time daily security openings under military protocol.
• Quality & Compliance Audit: Audited high-throughput partner onboarding records maintaining a 99.4% audited accuracy rate at Instawork while cutting review cycle times by 12%.
• Commercial Cost Reduction: Restructured vendor rate cards across 300+ deployments (15% recurring cost savings) and assisted leadership in closing INR 1.5L+ in commercial interior contracts (conferred written Management Commendation).

I have deployed a verified live portfolio showcase with interactive telemetry here:
https://github.com/AdityaMehra007

Would you or the hiring lead be open to a brief 10-minute introductory sync this week?

Warm regards,

Aditya Mehra
Phone: +91 70034 56624
LinkedIn: https://www.linkedin.com/in/adityamehra07
GitHub: https://github.com/AdityaMehra007
Bengaluru, India (Available Immediately)
"""

def generate_outreach_packets(limit: int = 25):
    if not APPROVAL_CSV.exists():
        print(f"[ERROR] Approval queue not found at {APPROVAL_CSV}")
        return

    staged_records = []
    with open(APPROVAL_CSV, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= limit:
                break
            
            person = row.get("Person", "Hiring Lead")
            first_name = person.split()[0] if person != "Hiring Lead" else "Hiring Team"
            company = row.get("Company", "Target Company")
            job_raw = row.get("Job", "Operations Specialist")
            job_title = job_raw.split(":")[-1].strip() if ":" in job_raw else job_raw

            message = HIGH_CONVERTING_TEMPLATE.format(
                first_name=first_name,
                company=company,
                title=job_title
            )

            record = {
                "action_id": row.get("Action ID", f"ACT-{i+1:04d}"),
                "recipient": person,
                "company": company,
                "job_title": job_title,
                "channel": row.get("Channel", "LinkedIn / Email"),
                "priority": row.get("Priority", "P0 - High Opportunity"),
                "outreach_text": message
            }
            staged_records.append(record)

    # Save to JSON
    out_file = OUTPUT_DIR / "staged_outreach_strikes.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(staged_records, f, indent=2)

    # Save clean readable summary markdown
    md_file = OUTPUT_DIR / "STAGED_OUTREACH_STRIKES.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("# 🚀 HIGH-PRIORITY RECRUITER OUTREACH STRIKES\n")
        f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total Staged: {len(staged_records)}*\n\n")
        for rec in staged_records:
            f.write(f"## [{rec['action_id']}] {rec['recipient']} — {rec['company']}\n")
            f.write(f"- **Target Role**: {rec['job_title']}\n")
            f.write(f"- **Channel**: {rec['channel']}\n")
            f.write(f"- **Priority**: {rec['priority']}\n\n")
            f.write("```text\n")
            f.write(rec["outreach_text"])
            f.write("\n```\n\n---\n\n")

    print(f"[SUCCESS] Staged {len(staged_records)} high-converting outreach strikes into:")
    print(f"  --> JSON: {out_file}")
    print(f"  --> Markdown: {md_file}")

if __name__ == "__main__":
    generate_outreach_packets(limit=30)
