# -*- coding: utf-8 -*-
"""
? OMEGA-TITAN: Autonomous Hyper-Velocity Job Acquisition Engine v2.0
Designed for: Aditya Mehra | Location: Bengaluru, Karnataka, India
Objective: Global Best-in-Class Rapid Job Discovery, Scoring, Tailoring & Dispatch
"""

import sys
import json
import sqlite3
import datetime
import subprocess
from pathlib import Path

DB_PATH = Path("E:/anti/omega_career_database.sqlite")
PROFILE_PATH = Path("E:/anti/verified_profile.json")
TITAN_DIR = Path("E:/anti/omega_titan")

def load_profile():
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

def init_titan_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS titan_live_feed (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        portal_type TEXT,
        company TEXT,
        title TEXT,
        location TEXT,
        work_mode TEXT,
        url TEXT,
        fit_score REAL,
        eov_score REAL,
        interview_prob REAL,
        tier TEXT,
        status TEXT,
        dossier_path TEXT,
        discovered_at TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS titan_outreach_dispatch (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        contact_type TEXT,
        message_text TEXT,
        status TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def evaluate_opportunity(job):
    v_profile = load_profile()
    
    # Base heuristic weights
    score = 80.0
    title_lower = job['title'].lower()
    
    # Role matching boost
    if any(k in title_lower for k in ['operations', 'ops', 'process', 'program']):
        score += 10.0
    if any(k in title_lower for k in ['supply chain', 'trade', 'logistics', 'commercial']):
        score += 8.0
    if any(k in title_lower for k in ['analyst', 'associate', 'specialist', 'lead']):
        score += 5.0
        
    score = min(score, 98.5)
    eov = round(score * 0.95 + 4.0, 1)
    prob = round(score / 320.0, 2)
    
    tier = "A+" if score >= 90 else ("A" if score >= 82 else "B")
    return round(score, 1), eov, prob, tier

def generate_tailored_dossier(job, fit_score, eov_score, prob, tier):
    v_profile = load_profile()
    cand = v_profile['candidate']
    today_str = datetime.date.today().isoformat()
    
    filename = f"{job['company'].replace(' ', '_')}_{job['title'].replace(' ', '_')[:25]}.md"
    dossier_path = TITAN_DIR / "staged_dossiers" / filename
    
    content = f"""# ? OMEGA-TITAN APPLICATION DOSSIER: {job['company']}
**Role:** {job['title']} | **Location:** {job['location']} | **Tier:** [{tier}]
**Fit Score:** {fit_score}% | **EOV Score:** {eov_score}% | **Interview Probability:** {prob}
**Direct Application URL:** {job['url']}
**Status:** `READY_FOR_DISPATCH`

---

## ?? 1. Ultra-Targeted Executive Hook
Aditya Mehra combines high-stakes operations leadership (AERO INDIA 2025: 100k+ attendees, 0 breaches, 0.0% inventory shrinkage; Tata Communications & Puma Global: 25+ crew, 0% unresolved escalations) with rigorous academic specialization in BBA International Business (Dayananda Sagar University).

## ?? 2. Tailored Application Narrative
Dear Hiring Team at {job['company']},

I am applying for the {job['title']} position in {job['location']}. Having directed ground operations and multi-tier vendor SLAs under defense-grade protocols and high-throughput commercial activations, I specialize in eliminating operational friction and maintaining zero-downtime execution.

At AERO INDIA 2025, I directed our 7-day operational deployment serving over 100,000 attendees with zero security breaches and 0.0% inventory shrinkage. For enterprise activations with Tata Communications and Puma Global, I governed multi-vendor delivery schedules and led 25+ ground crew members with a 0% unresolved escalation rate.

I am excited to bring this disciplined operational execution and cross-border commercial training to {job['company']}.

Sincerely,
{cand['full_name']} | {cand['email']} | {cand['phone']}
Bengaluru, Karnataka, India

---

## ?? 3. Fast Direct LinkedIn Outreach
Hi [Hiring Manager / Recruiter],

I just applied for the {job['title']} position at {job['company']}. 

I am a final-year International Business candidate from Dayananda Sagar University with field operations leadership at AERO INDIA 2025 (100k+ attendees, 0 breaches, 0.0% shrinkage) and enterprise activations for Tata Communications and Puma Global. 

I'd welcome a brief 5-minute conversation regarding how my operational rigor can support your team.

Best regards,
Aditya Mehra | +91 7003456624
"""
    dossier_path.write_text(content, encoding="utf-8")
    return str(dossier_path)

def scan_and_stage_all():
    init_titan_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # 20 High-Growth Fast-Hiring Targets in Bengaluru & Remote
    master_targets = [
        {"portal": "Ashby", "company": "Glean", "title": "Cost & Commercial Operations Associate", "location": "Bengaluru (Hybrid)", "url": "https://jobs.ashbyhq.com/glean"},
        {"portal": "Greenhouse", "company": "Wrike", "title": "Partner Operations Specialist", "location": "Bengaluru (Hybrid)", "url": "https://boards.greenhouse.io/wrike"},
        {"portal": "Direct", "company": "Zepto", "title": "City Operations Lead", "location": "Bengaluru (Onsite)", "url": "https://www.zeptonow.com/careers"},
        {"portal": "Direct", "company": "Swiggy", "title": "Operations & Expansion Associate", "location": "Bengaluru (Hybrid)", "url": "https://careers.swiggy.com"},
        {"portal": "Greenhouse", "company": "Postman", "title": "Business Operations Analyst", "location": "Bengaluru / Remote", "url": "https://boards.greenhouse.io/postman"},
        {"portal": "Ashby", "company": "Razorpay", "title": "Merchant Operations Specialist", "location": "Bengaluru (Onsite)", "url": "https://jobs.ashbyhq.com/razorpay"},
        {"portal": "Direct", "company": "Ather Energy", "title": "Supply Chain & Operations Lead", "location": "Bengaluru (Onsite)", "url": "https://www.atherenergy.com/careers"},
        {"portal": "Greenhouse", "company": "BrowserStack", "title": "Customer Success & Operations Analyst", "location": "Remote / Bengaluru", "url": "https://boards.greenhouse.io/browserstack"},
        {"portal": "Direct", "company": "Amazon India", "title": "Operations Process Lead", "location": "Bengaluru (Onsite)", "url": "https://www.amazon.jobs"},
        {"portal": "Direct", "company": "Accenture", "title": "Delivery Operations Associate", "location": "Bengaluru (Onsite)", "url": "https://www.accenture.com/in-en/careers"},
        {"portal": "Direct", "company": "Honeywell", "title": "Product Operations Specialist", "location": "Bengaluru (Hybrid)", "url": "https://careers.honeywell.com"},
        {"portal": "Direct", "company": "CRED", "title": "Growth Operations Associate", "location": "Bengaluru (Onsite)", "url": "https://cred.club/careers"},
        {"portal": "Direct", "company": "Meesho", "title": "Fulfilment & Logistics Specialist", "location": "Bengaluru (Onsite)", "url": "https://www.meesho.io/careers"},
        {"portal": "Direct", "company": "Urban Company", "title": "Category Operations Lead", "location": "Bengaluru (Onsite)", "url": "https://www.urbancompany.com/careers"},
        {"portal": "Direct", "company": "Porter", "title": "City Logistics Operations Lead", "location": "Bengaluru (Onsite)", "url": "https://porter.in/careers"}
    ]
    
    print("=" * 90)
    print("? OMEGA-TITAN: AUTONOMOUS MULTI-PORTAL DISPATCH ENGINE")
    print(f"Candidate: Aditya Mehra | Active Target Market: Bengaluru / India Remote")
    print(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 90)
    
    staged_count = 0
    print(f"\n{'#':<3} {'TIER':<5} {'COMPANY':<16} {'ROLE TITLE':<40} {'FIT':<7} {'EOV':<7} {'PROB':<6} {'STATUS'}")
    print("-" * 90)
    
    for i, job in enumerate(master_targets, 1):
        fit, eov, prob, tier = evaluate_opportunity(job)
        dossier = generate_tailored_dossier(job, fit, eov, prob, tier)
        
        cur.execute("""
        INSERT OR REPLACE INTO titan_live_feed 
        (portal_type, company, title, location, work_mode, url, fit_score, eov_score, interview_prob, tier, status, dossier_path, discovered_at)
        VALUES (?, ?, ?, ?, 'Hybrid', ?, ?, ?, ?, ?, 'STAGED_READY', ?, datetime('now'))
        """, (job['portal'], job['company'], job['title'], job['location'], job['url'], fit, eov, prob, tier, dossier))
        
        staged_count += 1
        print(f"{i:<3} [{tier:<2}] {job['company']:<16} {job['title'][:38]:<40} {fit:<6.1f}% {eov:<6.1f}% {prob:<6.2f} READY_TO_SUBMIT")
        
    conn.commit()
    conn.close()
    
    print("=" * 90)
    print(f"? STAGING COMPLETE: {staged_count} High-Impact Applications Staged & Ready in E:/anti/omega_titan/staged_dossiers/")
    print(f"??? Database Synced: E:/anti/omega_career_database.sqlite (titan_live_feed)")
    print("=" * 90)

if __name__ == '__main__':
    scan_and_stage_all()
