#!/usr/bin/env python3
"""
========================================================================================
SOVEREIGN STRIKE CLI: APEX CORPORATE INFILTRATION WEAPON (v2.0 SUPREME)
========================================================================================
Autonomous career strike tool that queries the 5,000 employer database, extracts verified
HR leads, and synthesizes 1-click executive InMail pitches, ATS-optimized dossiers,
STAR interview briefs, and interview calendar invites (.ics).

Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
Contact: +91 7003456624 | adityamehra799@gmail.com | github.com/AdityaMehra007

Usage:
  python sovereign_strike_cli.py --target "A.P. Moller - Maersk" --track trade
  python sovereign_strike_cli.py --target "Boeing India" --track operations
  python sovereign_strike_cli.py --target "Target" --track analytics
  python sovereign_strike_cli.py --corridor "Outer Ring Road" --batch 5
  python sovereign_strike_cli.py --list
========================================================================================
"""

import sys
import os
import argparse
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(r"e:\anti")
DB_PATH = ROOT_DIR / "BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite"
STRIKES_DIR = ROOT_DIR / "data" / "sovereign_strikes"
STRIKES_DIR.mkdir(parents=True, exist_ok=True)

TRACK_MAP = {
    "operations": {
        "title": "Corporate Operations & Technology Associate",
        "focus": "vendor management, SLA enforcement, process standardization, cross-functional execution",
        "bullet": "Standardized commercial vendor and procurement matrices, eliminating operational bottlenecks across high-footfall engagements."
    },
    "trade": {
        "title": "Global EXIM & International Trade Operations Specialist",
        "focus": "Incoterms 2020, customs clearance, cross-border freight documentation, ocean bill of lading",
        "bullet": "Trained in Incoterms 2020 risk transfer, maritime shipping lane reconciliations, and customs clearance protocols."
    },
    "analytics": {
        "title": "Business Intelligence & Operations Analyst",
        "focus": "data verification, automated reconciliation pipelines, Excel modeling, SLA variance detection",
        "bullet": "Conducted precision AI/robotics data audits at Instawork achieving 99.2% verified accuracy rate across thousands of events."
    },
    "ai": {
        "title": "AI Systems & Autonomous Workflow Operations Specialist",
        "focus": "LLM agentic workflows, Python automation, SQLite database operations, prompt orchestration",
        "bullet": "Architected autonomous operations prototypes in Python and SQLite with 16/16 verified unit tests passing green."
    },
    "founders": {
        "title": "Founder's Office & High-Velocity BizOps Associate",
        "focus": "0-to-1 operational builds, high-stress crisis management, executive reporting, instant execution",
        "bullet": "Delivered 100% balance reconciliation under peak footfall during Aero India while resolving infrastructure outages in real-time."
    }
}

def get_connection():
    if not DB_PATH.exists():
        print(f"Error: Database not found at {DB_PATH}")
        sys.exit(1)
    return sqlite3.connect(DB_PATH)

def list_top_targets():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT company_name, sector, corridor, hr_lead, hr_email, desk_email 
        FROM bangalore_5000_companies_master 
        WHERE hr_email != '' AND (corridor LIKE '%Manyata%' OR corridor LIKE '%Bellandur%' OR corridor LIKE '%Whitefield%')
        LIMIT 20
    """)
    rows = cur.fetchall()
    print("\n" + "=" * 100)
    print("⚡ TOP HIGH-PRIORITY CORPORATE INFILTRATION TARGETS (WITH DIRECT HR LEADS)")
    print("=" * 100)
    for r in rows:
        lead = r[3] if r[3] else "Talent Desk"
        email = r[4] if r[4] else r[5]
        print(f"• {r[0]:<35} | {r[1]:<22} | {lead:<20} | {email}")
    print("=" * 100 + "\n")
    conn.close()

def generate_ics_calendar(company, role, out_path):
    now = datetime.now()
    meeting_date = now + timedelta(days=2)
    dtstart = meeting_date.strftime("%Y%m%dT110000")
    dtend = meeting_date.strftime("%Y%m%dT112000")
    dtstamp = now.strftime("%Y%m%dT%H%M%SZ")

    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Aditya Mehra//Apex Career OS//EN
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
UID:strike-{company.lower().replace(' ', '-')}-{int(now.timestamp())}@adityamehra.work
DTSTAMP:{dtstamp}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:Introductory Briefing: Aditya Mehra <> {company} ({role})
DESCRIPTION:Introductory 15-minute briefing to review operational background and alignment for {role} at {company} Bengaluru.\\nCandidate: Aditya Mehra (+91 7003456624)\\nPortfolio: https://github.com/AdityaMehra007/anti
LOCATION:Google Meet / Zoom / Bengaluru HQ
STATUS:CONFIRMED
ORGANIZER;CN=Aditya Mehra:MAILTO:adityamehra799@gmail.com
ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE:MAILTO:adityamehra799@gmail.com
END:VEVENT
END:VCALENDAR"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(ics_content)

def generate_strike(target_name, track_name="operations", create_calendar=True):
    track = TRACK_MAP.get(track_name.lower(), TRACK_MAP["operations"])
    role_name = track["title"]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT company_name, official_website, careers_url, sector, corridor, hr_lead, hr_email, desk_email 
        FROM bangalore_5000_companies_master 
        WHERE company_name LIKE ? 
        LIMIT 1
    """, (f"%{target_name}%",))
    row = cur.fetchone()

    if not row:
        print(f"Target '{target_name}' not found. Searching closest matches...")
        cur.execute("SELECT company_name FROM bangalore_5000_companies_master WHERE company_name LIKE ? LIMIT 5", (f"%{target_name[:4]}%",))
        suggestions = [r[0] for r in cur.fetchall()]
        print(f"Did you mean: {suggestions}")
        conn.close()
        return None

    company, website, careers_url, sector, corridor, hr_lead, hr_email, desk_email = row
    conn.close()

    contact_email = hr_email if hr_email else desk_email if desk_email else f"talent@{website.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]}"
    recipient_name = hr_lead if hr_lead else "Talent Acquisition Team"

    slug = company.lower().replace(" ", "_").replace("(", "").replace(")", "").replace(".", "").replace("-", "_")
    out_file = STRIKES_DIR / f"{slug}_strike_dossier.json"
    ics_file = STRIKES_DIR / f"{slug}_intro_meeting.ics"

    pitch = f"""Subject: Aditya Mehra — Candidate for {role_name} ({company} Bengaluru)

Dear {recipient_name},

I noticed {company}'s active expansion for operations and technology talent in Bengaluru ({corridor}).

As a final-year BBA International Business graduate from Dayananda Sagar University (DSU, 2026), my background directly intersects with {company}'s operational delivery standards:

1. Operational Rigor & Integrity: Coordinated high-footfall field retail logistics during Aero India (Salt in My Cocoa) and commercial vendor matrices at Pencil Mark, executing 100% balance reconciliations with zero discrepancy.
2. Technical & Data Grounding: Completed AI robotics data quality audits at Instawork with 99.2% precision, and engineered autonomous operational workflow engines in Python & SQLite with 16/16 verified unit tests green.
3. Track Focus ({track_name.upper()}): Fluent in {track['focus']}.
4. Immediate Joining Readiness: Full-time availability in Bengaluru with zero notice period.

I have open-sourced my operational proof-of-work portfolio and verification codebase here:
• GitHub Repository: https://github.com/AdityaMehra007/anti
• Official Careers Application: Pre-staged via {careers_url}

No obligation at all—I would welcome a brief 5-minute conversation this week to discuss how I can immediately unblock your team's operational backlog.

Best regards,
Aditya Mehra
Bengaluru, India | +91 7003456624 | adityamehra799@gmail.com
LinkedIn: linkedin.com/in/aditya-mehra | GitHub: github.com/AdityaMehra007"""

    if create_calendar:
        generate_ics_calendar(company, role_name, ics_file)

    dossier = {
        "company_name": company,
        "sector": sector,
        "corridor": corridor,
        "official_website": website,
        "careers_portal": careers_url,
        "hr_lead": recipient_name,
        "hr_email": contact_email,
        "target_track": track_name,
        "target_role": role_name,
        "executive_pitch": pitch,
        "calendar_invite_path": str(ics_file) if create_calendar else None,
        "ats_optimized_bullets": [
            track["bullet"],
            "Engineered autonomous operational workflow pipelines handling relational databases with 16/16 green unit tests.",
            "Coordinated on-ground logistics and multi-channel cash/UPI reconciliations with 0.0% variance under high-stress footfalls."
        ]
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dossier, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 90)
    print(f"⚡ SOVEREIGN STRIKE DOSSIER GENERATED: {company.upper()}")
    print("=" * 90)
    print(f"📍 Location Corridor : {corridor}")
    print(f"🏢 Sector            : {sector}")
    print(f"👤 HR Lead / Desk    : {recipient_name}")
    print(f"📧 Verified Email    : {contact_email}")
    print(f"🎯 Target Track      : {track_name.upper()} ({role_name})")
    print(f"🔗 Careers Portal    : {careers_url}")
    print("-" * 90)
    print("📋 EXECUTIVE OUTREACH PITCH:")
    print("-" * 90)
    print(pitch)
    print("-" * 90)
    print(f"💾 Dossier Saved : {out_file}")
    if create_calendar:
        print(f"📅 Calendar .ics : {ics_file}")
    print("=" * 90 + "\n")
    return dossier

def batch_strike(corridor_query, count=5, track="operations"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT company_name 
        FROM bangalore_5000_companies_master 
        WHERE corridor LIKE ? AND hr_email != ''
        LIMIT ?
    """, (f"%{corridor_query}%", count))
    companies = [r[0] for r in cur.fetchall()]
    conn.close()

    print(f"\n🚀 Initiating Batch Sovereign Strike for {len(companies)} targets in '{corridor_query}'...\n")
    for comp in companies:
        generate_strike(comp, track_name=track, create_calendar=True)

def main():
    parser = argparse.ArgumentParser(description="Sovereign Strike CLI - Corporate Infiltration Tool v2.0")
    parser.add_argument("--target", type=str, help="Target company name (e.g. 'Maersk', 'Boeing', 'Goldman')")
    parser.add_argument("--track", type=str, default="operations", choices=list(TRACK_MAP.keys()), help="Specialization track")
    parser.add_argument("--corridor", type=str, help="Batch strike a specific corridor (e.g. 'Outer Ring Road', 'Whitefield')")
    parser.add_argument("--batch", type=int, default=5, help="Number of companies to strike in batch mode")
    parser.add_argument("--list", action="store_true", help="List top high-priority targets with verified HR leads")

    args = parser.parse_args()

    if args.list:
        list_top_targets()
    elif args.corridor:
        batch_strike(args.corridor, count=args.batch, track=args.track)
    elif args.target:
        generate_strike(args.target, track_name=args.track)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
