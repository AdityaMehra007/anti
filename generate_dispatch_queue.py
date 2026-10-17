#!/usr/bin/env python3
"""
Generates production-grade .eml dispatch files and master campaign ledger for Summer 2027 Cohort.
"""

import os
from datetime import datetime

TARGETS = [
    {
        "id": "APX-2027-001",
        "company": "Tesla",
        "role": "Data Analyst Intern - People Products",
        "email": "universityrecruiting@tesla.com",
        "recruiter": "Tesla University Talent Acquisition",
        "location": "Palo Alto, CA",
        "subject": "Candidate for Data Analyst Intern (Summer 2027) — Aditya Mehra",
        "highlight": "directed ground operations & dynamic dispatch tracking during Aero India 2025 and maintained 99%+ accuracy in AI quality benchmarks"
    },
    {
        "id": "APX-2027-002",
        "company": "TikTok / ByteDance",
        "role": "AI Governance Strategy Product Manager Intern",
        "email": "campus-us@tiktok.com",
        "recruiter": "TikTok University Relations Team",
        "location": "San Jose, CA",
        "subject": "Application: AI Governance Strategy PM Intern — Aditya Mehra",
        "highlight": "specialized in high-density governance, audit compliance, and multi-turn AI safety evaluations with 99%+ accuracy"
    },
    {
        "id": "APX-2027-003",
        "company": "Rivian",
        "role": "Supply Chain Data & AI Co-op Intern",
        "email": "talent@rivian.com",
        "recruiter": "Rivian Campus Recruiting",
        "location": "Normal, IL",
        "subject": "Prospective Intern: Supply Chain Data & AI — Aditya Mehra",
        "highlight": "hands-on experience managing multi-modal freight logistics, vendor staging, and time-critical supply lines for aerospace exhibitions"
    },
    {
        "id": "APX-2027-004",
        "company": "Intuit",
        "role": "Business Data Analyst Intern - Strategy & Planning",
        "email": "university_recruiting@intuit.com",
        "recruiter": "Intuit Campus Recruiting Lead",
        "location": "Mountain View, CA",
        "subject": "Candidate: Business Data Analyst Intern (Summer 2027) — Aditya Mehra",
        "highlight": "strong foundation in International Business (BBA 2026), unit economics modeling, and automated KPI reporting workflows"
    },
    {
        "id": "APX-2027-005",
        "company": "TikTok",
        "role": "Product Operations Intern - Apps & API",
        "email": "developer-campus@tiktok.com",
        "recruiter": "TikTok Developer Platform Recruiting",
        "location": "Seattle, WA",
        "subject": "Application: Product Operations Intern (Apps & API) — Aditya Mehra",
        "highlight": "managed live venue communications infrastructure and rapid SLA incident triage with Tata Communications"
    },
    {
        "id": "APX-2027-006",
        "company": "Tesla",
        "role": "Software Engineer Intern - Engineering Automation",
        "email": "engineeringrecruiting@tesla.com",
        "recruiter": "Tesla Autopilot & Engineering Recruiting",
        "location": "Palo Alto, CA",
        "subject": "Software Engineer Intern (Automation) — Aditya Mehra",
        "highlight": "engineered automated parsing and validation pipelines processing 17,000+ records with zero validation errors"
    },
    {
        "id": "APX-2027-007",
        "company": "Quantbot Technologies",
        "role": "Data Trading Analyst Intern",
        "email": "careers@quantbot.com",
        "recruiter": "Quantbot Talent Team",
        "location": "New York, NY",
        "subject": "Quantitative Application: Data Trading Analyst Intern — Aditya Mehra",
        "highlight": "developed systematic categorization pipelines across multi-source financial and market datasets"
    },
    {
        "id": "APX-2027-008",
        "company": "American Express",
        "role": "Product Manager / Business Analyst Intern",
        "email": "campusrecruiting@aexp.com",
        "recruiter": "American Express Campus Talent Acquisition",
        "location": "New York, NY",
        "subject": "Application: Product Manager / Business Analyst Intern — Aditya Mehra",
        "highlight": "specialized in international finance structures, cross-border payment compliance, and transaction governance"
    },
    {
        "id": "APX-2027-009",
        "company": "Waymo",
        "role": "Autonomous Fleet Operations Analyst Intern",
        "email": "waymo-campus@google.com",
        "recruiter": "Waymo University Recruiting",
        "location": "Mountain View, CA",
        "subject": "Prospective Intern: Autonomous Fleet Operations — Aditya Mehra",
        "highlight": "coordinated complex multi-vehicle motorcades and high-security fleet staging for 450+ delegates at Aero India 2025"
    },
    {
        "id": "APX-2027-010",
        "company": "AMD",
        "role": "Global Supply Chain Operations Analyst Intern",
        "email": "university.relations@amd.com",
        "recruiter": "AMD Global University Relations",
        "location": "Austin, TX",
        "subject": "Application: Global Supply Chain Operations Intern — Aditya Mehra",
        "highlight": "academic rigor in global supply chain management combined with zero-defect brand logistics execution for Puma Sports India"
    }
]

DISPATCH_DIR = r"e:\anti\reports\dispatch_queue\summer_2027_cohort"
os.makedirs(DISPATCH_DIR, exist_ok=True)

for i, t in enumerate(TARGETS, 1):
    eml_file = os.path.join(DISPATCH_DIR, f"{i:02d}_{t['company'].replace(' ', '_').replace('/', '_')}_{t['id']}.eml")
    eml_content = f"""To: {t['recruiter']} <{t['email']}>
From: Aditya Mehra <adityamehra007@gmail.com>
Subject: {t['subject']}
Date: {datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0530")}
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8

Dear {t['recruiter']},

I am writing to express my strong enthusiasm for the {t['role']} position at {t['company']} ({t['location']}).

With an academic foundation in International Business (BBA 2026) and a track record of high-stakes operational execution, I specialize in building structured, zero-defect data and logistics workflows. Specifically, I {t['highlight']}.

I have pre-packaged a comprehensive application dossier including:
1. Tailored ATS Resume (100% keyword alignment)
2. Role-specific 30-60-90 Day Execution Blueprint
3. STAR Interview Defense Framework

My full application dossier is prepared and available for review. I would welcome the opportunity to discuss how I can deliver immediate value to your team this summer.

Best regards,

Aditya Mehra
adityamehra007@gmail.com | +91-7003456624
Bangalore, India | Open to Relocation ({t['location']})
"""
    with open(eml_file, "w", encoding="utf-8") as f:
        f.write(eml_content)

print(f"Generated {len(TARGETS)} .eml dispatch files in {DISPATCH_DIR}!")

# Write Master Campaign Ledger
ledger_file = r"e:\anti\reports\SUMMER_2027_ELITE_CAMPAIGN_LEDGER.md"
ledger_content = f"""# SUMMER 2027 ELITE INTERNSHIP CAMPAIGN LEDGER
**Source**: SimplifyJobs/Summer2027-Internships  
**Candidate**: Aditya Mehra (`adityamehra007@gmail.com` | `+91-7003456624`)  
**Generated Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Target Dossiers Prepared**: 10

---

## 1. Target Dossiers & Status Board

| Ref ID | Target Company | Target Role | Location | Category | Compensation | Dossier Status | Dispatch EML |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `APX-2027-001` | **Tesla** | Data Analyst Intern - People Products | Palo Alto, CA | AI/ML/Data | $45 - $60/hr | `READY` | [01_Tesla.eml](file:///e:/anti/reports/dispatch_queue/summer_2027_cohort/01_Tesla_APX-2027-001.eml) |
| `APX-2027-002` | **TikTok / ByteDance** | AI Governance Strategy PM Intern | San Jose, CA | Product | $55 - $72/hr | `READY` | [02_TikTok.eml](file:///e:/anti/reports/dispatch_queue/summer_2027_cohort/02_TikTok___ByteDance_APX-2027-002.eml) |
| `APX-2027-003` | **Rivian** | Supply Chain Data & AI Co-op Intern | Normal, IL | AI/Supply Chain | $42 - $55/hr | `READY` | [03_Rivian.eml](file:///e:/anti/reports/dispatch_queue/summer_2027_cohort/03_Rivian_APX-2027-003.eml) |
| `APX-2027-004` | **Intuit** | Business Data Analyst Intern | Mountain View, CA | AI/ML/Data | $48 - $62/hr | `READY` | [04_Intuit.eml](file:///e:/anti/reports/dispatch_queue/summer_2027_cohort/04_Intuit_APX-2027-004.eml) |
| `APX-2027-005` | **TikTok** | Product Operations Intern - Apps & API | Seattle, WA | Product Ops | $50 - $65/hr | `READY` | [05_TikTok.eml](file:///e:/anti/reports/dispatch_queue/summer_2027_cohort/05_TikTok_APX-2027-005.eml) |
| `APX-2027-006` | **Tesla** | Software Engineer Intern - Automation | Palo Alto, CA | Software/Auto | $50 - $68/hr | `READY` | [06_Tesla.eml](file:///e:/anti/reports/dispatch_queue/summer_2027_cohort/06_Tesla_APX-2027-006.eml) |
| `APX-2027-007` | **Quantbot Technologies** | Data Trading Analyst Intern | New York, NY | Quant Finance | $55 - $75/hr | `READY` | [07_Quantbot.eml](file:///e:/anti/reports/dispatch_queue/summer_2027_cohort/07_Quantbot_Technologies_APX-2027-007.eml) |
| `APX-2027-008` | **American Express** | Product Manager / Business Analyst Intern | New York, NY | Product/FinTech | $45 - $58/hr | `READY` | [08_Amex.eml](file:///e:/anti/reports/dispatch_queue/summer_2027_cohort/08_American_Express_APX-2027-008.eml) |
| `APX-2027-009` | **Waymo** | Autonomous Fleet Operations Analyst | Mountain View, CA | Fleet Ops | $48 - $64/hr | `READY` | [09_Waymo.eml](file:///e:/anti/reports/dispatch_queue/summer_2027_cohort/09_Waymo_APX-2027-009.eml) |
| `APX-2027-010` | **AMD** | Global Supply Chain Operations Intern | Austin, TX | Hardware/SCM | $44 - $56/hr | `READY` | [10_AMD.eml](file:///e:/anti/reports/dispatch_queue/summer_2027_cohort/10_AMD_APX-2027-010.eml) |

---

## 2. Dossier Asset Structure per Target
Each target directory in `applications_generated/` contains 8 standardized, high-conviction files:
1. `APPLICATION_MANIFEST.json` — Machine-readable tracking specification
2. `MASTER_CONQUEST_INDEX.md` — Strategic conquest brief and target checklist
3. `ATS_RESUME.md` — 100% ATS keyword-tailored resume
4. `COVER_LETTER.md` — Executive cover letter aligned with company mission
5. `DIRECT_OUTREACH_INMAIL.md` — Recruiter & Hiring Manager cold sequence
6. `STAR_INTERVIEW_DEFENSE.md` — 5 rigorously structured behavioral and technical answers
7. `DAY_30_60_90_PLAN.md` — Concrete execution roadmap for the internship
8. `COMPENSATION_NEGOTIATION.md` — Relocation, stipend, and conversion defense

---

## 3. Quick Action Execution
- **Launch Interactive Dashboard**: `python summer_2027_engine.py --dashboard`
- **Inspect Target Packages**: Explore `e:\anti\applications_generated\APX-2027-*`
- **Send Outreach**: Dispatched `.eml` drafts available under `e:\anti\reports\dispatch_queue\summer_2027_cohort\`
"""

with open(ledger_file, "w", encoding="utf-8") as f:
    f.write(ledger_content)

print(f"Generated master campaign ledger at {ledger_file}!")
