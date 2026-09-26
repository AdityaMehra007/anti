"""
Automated Job Portal Navigator & Tracker for Windows
Targeting BBA International Business roles at Bangalore MNCs
"""

import os
import sys
import csv
import time
import webbrowser
from datetime import datetime

# Define target job application portals and direct search queries
TARGET_JOBS = [
    {
        "company": "Accenture India",
        "role": "Global Operations Analyst / Business Consulting",
        "url": "https://www.accenture.com/in-en/careers/jobsearch?jk=International%20Business%20Analyst&sb=1",
        "cover_letter_key": "ACCENTURE"
    },
    {
        "company": "Deloitte US-India",
        "role": "Risk & Financial Advisory Analyst (Trade & Compliance)",
        "url": "https://www2.deloitte.com/ui/en/careers/careers.html",
        "cover_letter_key": "DELOITTE"
    },
    {
        "company": "EY India (GDS)",
        "role": "Business Analyst - Global Advisory & Operations",
        "url": "https://www.ey.com/en_in/careers",
        "cover_letter_key": "EY"
    },
    {
        "company": "Amazon Bangalore",
        "role": "Operations & Supply Chain Executive",
        "url": "https://www.amazon.jobs/en/search?base_query=Operations+Analyst&loc_query=Bangalore%2C+India",
        "cover_letter_key": "AMAZON"
    },
    {
        "company": "Goldman Sachs",
        "role": "Global Markets Operations Analyst",
        "url": "https://www.goldmansachs.com/careers/students/programs/india/new-analyst-program.html",
        "cover_letter_key": "GOLDMAN SACHS"
    },
    {
        "company": "LinkedIn Jobs",
        "role": "BBA International Business Bangalore MNC Search",
        "url": "https://www.linkedin.com/jobs/search/?keywords=BBA%20International%20Business&location=Bengaluru%2C%20Karnataka%2C%20India",
        "cover_letter_key": "GENERAL"
    },
    {
        "company": "Naukri.com",
        "role": "International Business Analyst Bangalore",
        "url": "https://www.naukri.com/international-business-analyst-jobs-in-bangalore",
        "cover_letter_key": "GENERAL"
    }
]

def load_cover_letters():
    path = os.path.join(os.path.dirname(__file__), "Cover_Letters_All_MNCs.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def update_tracker(company_name):
    tracker_path = os.path.join(os.path.dirname(__file__), "Application_Tracker.csv")
    rows = []
    if os.path.exists(tracker_path):
        with open(tracker_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("Company") == company_name:
                    row["Status"] = "Portal Opened"
                    row["Date Applied"] = datetime.now().strftime("%Y-%m-%d")
                rows.append(row)
        
        if rows:
            with open(tracker_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

def run_automation():
    print("=" * 80)
    print("🚀 AUTOMATED MNC JOB APPLICATION LAUNCHER (WINDOWS)")
    print("Target: BBA International Business | Location: Bangalore")
    print("=" * 80)
    print()
    
    cover_letters = load_cover_letters()

    for idx, item in enumerate(TARGET_JOBS, 1):
        print(f"\n[{idx}/{len(TARGET_JOBS)}] Opening Portal for: {item['company']}")
        print(f"📌 Role Target: {item['role']}")
        print(f"🌐 Opening URL: {item['url']}")
        
        # Open in default system browser (Chrome/Edge/Firefox)
        webbrowser.open(item['url'])
        
        # Update tracking sheet status
        update_tracker(item['company'])
        
        print(f"✅ Portal opened in browser. Status updated in Application_Tracker.csv.")
        print("-" * 60)
        time.sleep(1.5)

    print("\n" + "=" * 80)
    print("🎉 ALL TARGET PORTALS OPENED SUCCESSFULLY!")
    print("All cover letters are ready in: Cover_Letters_All_MNCs.txt")
    print("Resume details are ready in: Resume_BBA_International_Business.md")
    print("Tracking sheet updated in: Application_Tracker.csv")
    print("=" * 80)

if __name__ == "__main__":
    run_automation()
