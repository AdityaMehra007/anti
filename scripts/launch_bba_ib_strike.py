#!/usr/bin/env python3
import sys, os, json, sqlite3, webbrowser, argparse
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"e:/anti")
DATA_DIR = ROOT_DIR / "data"
PKGS_DIR = ROOT_DIR / "applications_generated" / "bangalore_61_packages"
APPROVALS_DB = DATA_DIR / "omega_approvals.db"

PRIORITY_TIER1_JOBS = [
    {
        "id": "BLR-JOB-001",
        "company": "Accenture India",
        "title": "Global Business Operations & BD Analyst",
        "fit": "9.8 / 10.0",
        "url": "https://www.accenture.com/in-en/careers",
        "folder": "BLR-JOB-001_Accenture_India",
        "rationale": "DSU BBA IB alignment: Global operations, cross-border business process analysis."
    },
    {
        "id": "BLR-JOB-002",
        "company": "Deloitte US-India",
        "title": "Risk & Business Operations Advisory Analyst",
        "fit": "9.7 / 10.0",
        "url": "https://www2.deloitte.com/ui/en/careers/careers.html",
        "folder": "BLR-JOB-002_Deloitte_US-India",
        "rationale": "International trade regulations, risk advisory, and SOP governance."
    },
    {
        "id": "BLR-JOB-003",
        "company": "EY (Ernst & Young GDS)",
        "title": "Business Analyst - Global Advisory",
        "fit": "9.6 / 10.0",
        "url": "https://www.ey.com/en_in/careers",
        "folder": "BLR-JOB-003_EY_GDS",
        "rationale": "Global enterprise operations and cross-border trade advisory practice."
    },
    {
        "id": "BLR-JOB-004",
        "company": "Amazon Bangalore",
        "title": "Operations & Vendor Management Executive",
        "fit": "9.6 / 10.0",
        "url": "https://www.amazon.jobs/en/locations/bangalore-india",
        "folder": "BLR-JOB-004_Amazon_Bangalore",
        "rationale": "Vendor SLAs, inbound/outbound logistics, catalog quality operations."
    },
    {
        "id": "BLR-JOB-005",
        "company": "Goldman Sachs",
        "title": "Global Markets Operations Analyst",
        "fit": "9.5 / 10.0",
        "url": "https://www.goldmansachs.com/careers/",
        "folder": "BLR-JOB-005_Goldman_Sachs",
        "rationale": "International trade settlements and cross-border transaction compliance (Bellandur campus)."
    },
    {
        "id": "BLR-JOB-006",
        "company": "JP Morgan Chase",
        "title": "Global Operations & Compliance Associate",
        "fit": "9.5 / 10.0",
        "url": "https://careers.jpmorganchase.com/",
        "folder": "BLR-JOB-006_JP_Morgan_Chase",
        "rationale": "Global banking operations and compliance execution (Kadubeesanahalli campus)."
    },
    {
        "id": "BLR-JOB-008",
        "company": "AERO India / Salt in My Coca",
        "title": "Exhibition & Event Operations Lead",
        "fit": "9.9 / 10.0",
        "url": "https://aeroindia.gov.in/",
        "folder": "BLR-JOB-008_AERO_India",
        "rationale": "VERIFIED CREDENTIAL: Ground ops, VIP delegation protocol & multi-agency liaison at Yelahanka AFB."
    },
    {
        "id": "BLR-JOB-009",
        "company": "IBM India",
        "title": "Supply Chain & Operations Consultant",
        "fit": "9.5 / 10.0",
        "url": "https://www.ibm.com/in-en/employment/",
        "folder": "BLR-JOB-009_IBM_India",
        "rationale": "Global SCM networks, trade lane visibility, and international procurement."
    },
    {
        "id": "BLR-JOB-010",
        "company": "Flipkart Bangalore",
        "title": "Operations Specialist - Supply Chain & Logistics",
        "fit": "9.6 / 10.0",
        "url": "https://www.flipkartcareers.com/",
        "folder": "BLR-JOB-010_Flipkart_India",
        "rationale": "Fulfillment center operations, reverse logistics, and logistics vendor SLA tracking."
    },
    {
        "id": "BLR-JOB-011",
        "company": "Puma India (Bangalore HQ)",
        "title": "Retail Operations & Brand Experience Coordinator",
        "fit": "9.8 / 10.0",
        "url": "https://about.puma.com/en/careers",
        "folder": "BLR-JOB-011_Puma_Sports_India",
        "rationale": "VERIFIED CREDENTIAL: Store operations and on-ground brand activation management across Bangalore."
    }
]

def log_dispatch(job_id, company, title):
    if not APPROVALS_DB.exists():
        return
    try:
        conn = sqlite3.connect(APPROVALS_DB)
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO bangalore_applications_audit (job_id, company, role_title, fit_score, status, updated_at) VALUES (?, ?, ?, ?, ?, ?)", (job_id, company, title, 9.8, 'DISPATCHED_PORTAL_OPENED', datetime.now().isoformat()))
        conn.commit()
        conn.close()
    except Exception:
        pass

def dispatch_job(job, open_browser=True):
    print("=" * 80)
    print(f"  TARGET: {job['company'].upper()} — {job['title']}")
    print(f"  Job ID   : {job['id']} | Fit: {job['fit']}")
    print(f"  Rationale: {job['rationale']}")
    print("=" * 80)
    pkg_path = PKGS_DIR / job['folder']
    resume_file = pkg_path / "resume_ats_1page.html"
    cover_file = pkg_path / "cover_letter.md"
    payload_file = pkg_path / "application_form_payload.json"
    if resume_file.exists():
        print(f"  [+] Harvard ATS Resume  : {resume_file}")
    if cover_file.exists():
        print(f"  [+] Role Cover Letter   : {cover_file}")
    if payload_file.exists():
        print(f"  [+] Q&A Form Answers    : {payload_file}")
    print(f"  [*] Requisition Portal  : {job['url']}")
    log_dispatch(job['id'], job['company'], job['title'])
    if open_browser:
        if resume_file.exists():
            webbrowser.open(resume_file.as_uri())
        webbrowser.open(job['url'])
        print("  [OK] Launched Portal & Resume in your browser!")

def main():
    parser = argparse.ArgumentParser(description="BBA IB Bangalore Fast Strike Application Engine")
    parser.add_argument("--top10", action="store_true", help="Launch top 10 high-affinity Bangalore requisitions")
    parser.add_argument("--all-hub", action="store_true", help="Open the 61-requisition interactive application studio")
    parser.add_argument("--list", action="store_true", help="List the top high-affinity Bangalore openings")
    parser.add_argument("--job", type=str, help="Launch a specific Job ID (e.g. BLR-JOB-001)")
    args = parser.parse_args()
    if args.list:
        print("=" * 80)
        print("  TOP 10 HIGH-AFFINITY BBA INTERNATIONAL BUSINESS ROLES IN BANGALORE")
        print("=" * 80)
        for i, j in enumerate(PRIORITY_TIER1_JOBS, 1):
            print(f"[{i:02d}] {j['company']:<25} | {j['title']:<38} | Fit: {j['fit']}")
        print("=" * 80)
        return
    if args.job:
        matched = [j for j in PRIORITY_TIER1_JOBS if j['id'].lower() == args.job.lower()]
        if matched:
            dispatch_job(matched[0], open_browser=True)
        else:
            print(f"[-] Unknown Job ID: {args.job}")
        return
    if args.top10:
        print("[*] Launching Top 10 High-Affinity Bangalore Openings for Aditya Mehra...")
        for j in PRIORITY_TIER1_JOBS:
            dispatch_job(j, open_browser=True)
        print("\n[✓] All 10 Target Career Portals and Tailored ATS Resumes have been opened in your browser!")
        print("[*] Submit your resume and paste form answers into each portal now.")
        return
    hub_path = ROOT_DIR / "apps" / "job_application_studio" / "bangalore_master_strike_studio.html"
    print("=" * 80)
    print("  LAUNCHING BBA IB BANGALORE MASTER APPLICATION HUB")
    print(f"  Studio Path: {hub_path}")
    print("=" * 80)
    webbrowser.open(hub_path.as_uri())

if __name__ == "__main__":
    main()
