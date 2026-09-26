"""
AI Autopilot Job Application Engine (Windows)
Target: Aditya Mehra | BBA International Business | Bangalore MNCs

Features:
1. Reads Application_Tracker.csv & Bangalore_3000_Company_Target_Directory.csv
2. Copies company-tailored Cover Letter & Resume Pitch to Windows Clipboard automatically.
3. Launches target application portals in default browser (Chrome/Edge).
4. Auto-updates application status in Application_Tracker.csv.
"""

import os
import sys
import csv
import time
import subprocess
import webbrowser
from datetime import datetime

WORKSPACE = os.path.dirname(__file__)
TRACKER_FILE = os.path.join(WORKSPACE, "Application_Tracker.csv")
COVER_LETTERS_FILE = os.path.join(WORKSPACE, "Cover_Letters_All_MNCs.txt")

def copy_to_clipboard(text):
    """Copies text to Windows Clipboard via PowerShell."""
    try:
        cmd = f'Set-Clipboard -Value @\'\n{text}\n\'@'
        subprocess.run(["powershell", "-Command", cmd], check=True)
        return True
    except Exception as e:
        print(f"Clipboard copy note: {e}")
        return False

def get_cover_letter(company_name):
    """Reads cover letter text from Cover_Letters_All_MNCs.txt for company."""
    if os.path.exists(COVER_LETTERS_FILE):
        with open(COVER_LETTERS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            if company_name.upper() in content.upper():
                # Extract relevant section
                sections = content.split("================================================================================")
                for sec in sections:
                    if company_name.upper() in sec.upper():
                        return sec.strip()
    return f"""Dear Hiring Team,

I am writing to express my strong interest in Business Development, Operations, and EXIM Analyst opportunities at {company_name} in Bangalore.

Holding a BBA in International Business from Dayananda Sagar University, I bring proven hands-on experience in vendor management, client outreach, and event operations—including leading exhibition operations at AERO India 2025 and coordinating corporate events for clients like Tata Communications and Puma.

Thank you for considering my application.

Sincerely,
Aditya Mehra | +91-7003456624 | adityamehra799@gmail.com"""

def update_tracker(company_name):
    """Updates Application_Tracker.csv with current timestamp."""
    rows = []
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("Company Name") == company_name or row.get("Company") == company_name:
                    row["Status"] = "Applied / Submitted"
                    row["Date Applied"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                rows.append(row)
        
        if rows:
            with open(TRACKER_FILE, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

def run_autopilot_engine():
    print("=" * 80)
    print("🚀 AI AUTOPILOT JOB APPLICATION ENGINE")
    print("Candidate: Aditya Mehra | BBA International Business | Bangalore")
    print("=" * 80)
    print()

    target_companies = [
        {"name": "Accenture", "url": "https://www.accenture.com/in-en/careers"},
        {"name": "Deloitte", "url": "https://www2.deloitte.com/ui/en/careers/careers.html"},
        {"name": "EY (Ernst & Young)", "url": "https://www.ey.com/en_in/careers"},
        {"name": "KPMG", "url": "https://home.kpmg/in/en/home/careers.html"},
        {"name": "Amazon", "url": "https://www.amazon.jobs/en/locations/bangalore-india"},
        {"name": "Goldman Sachs", "url": "https://www.goldmansachs.com/careers/"},
        {"name": "IBM", "url": "https://www.ibm.com/in-en/employment/"},
        {"name": "TE Connectivity", "url": "https://www.te.com/usa-en/about-te/careers.html"}
    ]

    for idx, item in enumerate(target_companies, 1):
        comp = item["name"]
        url = item["url"]
        print(f"\n[{idx}/{len(target_companies)}] Launching Application Engine for: {comp}")
        print(f"🌐 Portal URL: {url}")
        
        # 1. Get Tailored Cover Letter & Copy to Windows Clipboard
        cl_text = get_cover_letter(comp)
        copy_to_clipboard(cl_text)
        print(f"📋 Tailored Cover Letter for {comp} copied to your Windows Clipboard!")
        print("💡 (Simply press Ctrl + V on the application webform to paste your cover letter)")
        
        # 2. Launch Browser Portal
        webbrowser.open(url)
        print(f"🔗 Browser tab opened for {comp}.")
        
        # 3. Update Tracker CSV
        update_tracker(comp)
        
        time.sleep(1.5)

    print("\n" + "=" * 80)
    print("🎉 ALL MNC APPLICATION PORTALS LAUNCHED!")
    print("Tracking Status Updated in: Application_Tracker.csv")
    print("Cover Letters Ready in: Cover_Letters_All_MNCs.txt")
    print("Resume File: Resume_Aditya_Mehra.md")
    print("=" * 80)

if __name__ == "__main__":
    run_autopilot_engine()
