#!/usr/bin/env python3
"""
========================================================================================
BANGALORE JOB AGENCIES & RECRUITER PLACEMENT CONTROLLER
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
========================================================================================
Automates candidate registration, agency portal access, and specialized headhunter
outreach across top Bangalore staffing firms & placement consultancies:
  - Michael Page, Randstad, Adecco, CareerNet, ABC Consultants, TeamLease, Quess, etc.
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import csv
import webbrowser
import argparse
from pathlib import Path
from email.message import EmailMessage

ROOT_DIR = Path(r"e:/anti")
DATA_DIR = ROOT_DIR / "data"
AGENCIES_JSON = DATA_DIR / "bangalore_job_agencies.json"
AGENCY_EML_DIR = ROOT_DIR / "applications_generated" / "agency_eml_outbox"
STUDIO_PATH = ROOT_DIR / "apps" / "job_application_studio" / "bangalore_agency_studio.html"

def load_agencies():
    if AGENCIES_JSON.exists():
        with open(AGENCIES_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def cmd_status():
    agencies = load_agencies()
    print("=" * 80)
    print("  BANGALORE RECRUITMENT AGENCIES & PLACEMENT CONSULTANCIES DIRECTORY")
    print(f"  Candidate: Aditya Mehra | BBA International Business (DSU '26)")
    print("=" * 80)
    print(f"[*] Curated Top Bangalore Agencies : {len(agencies)} Active Placement Firms")
    print(f"[*] Candidate Positioning         : Operations / Supply Chain / EXIM / AI Data")
    print(f"[*] Strict Guardrail              : 100% Sales Exclusion (No Cold Calling / Telecalling)")
    print("=" * 80)
    for i, a in enumerate(agencies, 1):
        specs = ", ".join(a["specializations"][:2])
        print(f"[{i:02d}] {a['name']:<42} | {a['location']:<32} | Specs: {specs}")
    print("=" * 80)

def cmd_open_portals():
    agencies = load_agencies()
    print("=" * 80)
    print(f"[*] Launching Top {len(agencies)} Bangalore Agency Registration Portals in Browser...")
    print("=" * 80)
    for a in agencies:
        print(f"  [+] Opening {a['name']}: {a['portal_url']}")
        webbrowser.open(a['portal_url'])
    print("\n[✓] All agency registration portals opened in your browser!")
    print("[*] Upload your 1-page Harvard ATS resume on each portal.")

def generate_agency_emails(agencies=None) -> int:
    if agencies is None:
        agencies = load_agencies()
    AGENCY_EML_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for a in agencies:
        eml_file = AGENCY_EML_DIR / f"{a['id']}_{a['name'].replace(' ', '_').replace('/', '_')}.eml"
        
        msg = EmailMessage()
        msg["From"] = "Aditya Mehra <adityamehra799@gmail.com>"
        msg["To"] = a["email"]
        msg["Subject"] = f"Candidate Profile for Bangalore Client Mandates: Aditya Mehra (BBA IB '26 | DSU)"
        msg["Date"] = "Fri, 11 Sep 2026 14:55:00 +0530"
        
        body = f"""Dear Recruitment Team at {a['name']},

I hope this email finds you well.

I am writing to register my candidate profile for ongoing and upcoming Bangalore corporate client mandates across Global Business Operations, Supply Chain & Logistics, and Business Analyst tracks.

CANDIDATE SNAPSHOT:
• Candidate: Aditya Mehra
• Degree: BBA in International Business, Dayananda Sagar University (DSU), Bengaluru (Class of 2026)
• Availability: Immediate Joining | Location: Bengaluru, Karnataka
• Target Domains: Operations Analyst, Supply Chain Associate, EXIM Operations, Brand & Ground Ops Lead (Strictly Non-Sales)

VERIFIED CREDENTIAL HIGHLIGHTS:
1. High-Stakes Ground Operations: Ground Operations & Protocol Lead at Aero India 2025 (Air Force Station Yelahanka) managing crowd logistics, Tier-1 vendor SLAs, and VIP security triage for 100k+ attendees.
2. Retail & Brand Activations: Spearheaded operational logistics, inventory intake, and POS tracking for Puma Global, Tata Communications, and Decathlon activations across Bangalore.
3. AI Platform Quality Operations: QA validation, error taxonomy, and annotation workflows at Instawork achieving 99%+ accuracy benchmarks.
4. International Trade Rigor: Grounded in Incoterms 2020, customs clearance, bill of lading, and freight landed cost optimization.

If your agency represents corporate MNCs, GCCs, or high-growth Bangalore enterprises with operational requirements, I would welcome the opportunity to connect.

Attached is my tailored 1-page Harvard ATS resume for your talent pool.

Warm regards,
Aditya Mehra
+91 70034 56624 | adityamehra799@gmail.com
LinkedIn: https://www.linkedin.com/in/adityamehra07
Bengaluru, Karnataka, India
"""
        msg.set_content(body)
        with open(eml_file, "wb") as f:
            f.write(msg.as_bytes())
        count += 1
    return count

def cmd_generate_agency_emails():
    print(f"[*] Generating tailored headhunter RFC-822 .eml drafts in: {AGENCY_EML_DIR}")
    count = generate_agency_emails()
    print(f"[✓] Successfully generated {count} headhunter outreach .eml drafts!")
    print("[*] Double-click any file in applications_generated/agency_eml_outbox/ to send via Outlook/Mail.")

def export_csv(agencies=None) -> Path:
    if agencies is None:
        agencies = load_agencies()
    csv_file = ROOT_DIR / "BANGALORE_JOB_AGENCIES_MASTER.csv"
    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Agency ID", "Agency Name", "Tier / Category", "Bangalore Location Hub", "Practice Specializations", "Candidate Portal URL", "Agency Contact Email", "Desk Phone", "Pitch Summary"])
        for a in agencies:
            writer.writerow([
                a["id"], a["name"], a["tier"], a["location"], "; ".join(a["specializations"]),
                a["portal_url"], a["email"], a["desk_phone"], a["agency_pitch"]
            ])
    return csv_file

def cmd_export_csv():
    csv_file = export_csv()
    print(f"[+] Exported master agency CSV to: {csv_file}")

def cmd_open_studio():
    if STUDIO_PATH.exists():
        print(f"[*] Opening Bangalore Agency & Headhunter Strike Studio: {STUDIO_PATH}")
        webbrowser.open(STUDIO_PATH.as_uri())
    else:
        print(f"[-] Studio file not found at {STUDIO_PATH}")

def main():
    parser = argparse.ArgumentParser(description="Bangalore Job Agencies & Placement Controller")
    parser.add_argument("--status", action="store_true", help="Display all curated Bangalore agencies")
    parser.add_argument("--open-portals", action="store_true", help="Open candidate registration portals in browser")
    parser.add_argument("--generate-agency-emails", action="store_true", help="Generate ready .eml drafts for agencies")
    parser.add_argument("--export-agency-csv", action="store_true", help="Export clean CSV of all agencies")
    parser.add_argument("--open-agency-studio", action="store_true", help="Open interactive Agency Strike Studio in browser")
    
    args = parser.parse_args()
    
    if args.status:
        cmd_status()
    elif args.open_portals:
        cmd_open_portals()
    elif args.generate_agency_emails:
        cmd_generate_agency_emails()
    elif args.export_agency_csv:
        cmd_export_csv()
    elif args.open_agency_studio or len(sys.argv) == 1:
        cmd_open_studio()

if __name__ == "__main__":
    main()
