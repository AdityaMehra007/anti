#!/usr/bin/env python3
"""
========================================================================================
ANTIGRAVITY APEX CAREER OS: ATS AUTO-FILL & COPILOT PRE-FILL ENGINE
========================================================================================
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
Function:
  Generates production-ready, standardized auto-fill payloads for Greenhouse,
  Workday, Lever, SmartRecruiters, and Taleo across the top 30 target enterprises.
  Emulates Simplify+ and Teal+ autofill without browser extension dependencies.
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
DATA_DIR = ROOT_DIR / "data"
OUT_JSON = DATA_DIR / "ats_autofill_payloads_master.json"
OUT_MD = ROOT_DIR / "ATS_AUTOFILL_PREFILL_DOSSIER.md"

CANDIDATE = {
    "first_name": "Aditya",
    "last_name": "Mehra",
    "full_name": "Aditya Mehra",
    "email": "adityamehra007@gmail.com",
    "alt_email": "adityamehra799@gmail.com",
    "phone": "+91 7003456624",
    "country_code": "+91",
    "location": {
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "postal_code": "560068"
    },
    "linkedin": "https://www.linkedin.com/in/adityamehra",
    "portfolio": "https://adityamehra.career",
    "github": "https://github.com/adityamehra",
    "work_authorization": {
        "citizen_of_india": True,
        "require_sponsorship": False,
        "eligible_to_work_in_india": True,
        "notice_period_days": 0,
        "available_from": "Immediate / Fresher Cohort 2026",
        "willing_to_relocate": True,
        "preferred_location": "Bengaluru, Karnataka"
    },
    "education": {
        "degree": "Bachelor of Business Administration (BBA)",
        "major": "International Business",
        "institution": "Dayananda Sagar University (DSU), Bengaluru",
        "start_year": 2023,
        "graduation_year": 2026,
        "gpa": "First Class / Distinction"
    },
    "eeo": {
        "gender": "Male",
        "veteran_status": "No",
        "disability_status": "No"
    },
    "compensation": {
        "expected_ctc_inr": "₹7,500,000 - ₹9,500,000 LPA (₹7.5L - ₹9.5L)",
        "currency": "INR",
        "flexible": True
    }
}

ESSAY_BANK = {
    "why_company": "I have closely tracked {company}'s operational leadership and technological scale in Bengaluru. With my proven experience coordinating high-stakes ground operations at Aero India 2025, structuring tier-1 vendor rate cards to achieve a 15% cost reduction, and executing multi-modal AI dataset quality at Instawork AI, I am eager to apply this rigorous operational discipline to deliver immediate, measurable value at {company}.",
    "biggest_challenge": "During Aero India 2025 at Yelahanka Air Force Station, a critical tier-1 audio-visual vendor was stalled at the gate due to vehicle pass discrepancies 90 minutes before VIP walkthrough. I decoupled the physical delivery from the commercial dispute: dispatched our liaison with master manifests to Gate 4, authorized manual perimeter unloading to bypass staging bottlenecks, and directed the booth team to configure backup gear. We completed setup at 07:22 AM (8 mins ahead of deadline) with 100% uptime and 0% shrinkage across ₹12.5L inventory.",
    "conflict_resolution": "When a long-term merchandise supplier issued an uncontracted 12.5% surcharge invoice right before a client activation, I avoided an operational halt by issuing an immediate voucher for the undisputed contracted amount under clause 4.2 of our MSA. Concurrently, I conducted an algorithmic rate card reconciliation proving the price surge was uncontracted. The vendor released goods on time, and we preserved the ₹15,000 margin (11.1% cost avoidance) without damaging the vendor relationship.",
    "strength": "My greatest strength is end-to-end operational execution combined with quantitative cost governance. Having led 300+ on-ground deployments with zero budget overruns and driven an audited 99%+ AI QA accuracy at Instawork AI, I operate with high agency, meticulous process documentation, and rapid problem triage.",
    "future_goals": "Over the next 2-3 years, my goal is to master enterprise process optimization and global supply chain execution as a core contributor at {company}, advancing toward operational team leadership and driving scalable automation across international service delivery."
}

TARGET_COMPANIES = [
    {"name": "Deloitte US-India", "portal_type": "Workday", "job_id": "Req #59664844", "role": "Risk & Business Operations Advisory Analyst"},
    {"name": "Boeing India (BIETC)", "portal_type": "Workday", "job_id": "BOE-IND-SCM-0881", "role": "Associate Procurement & SCM Analyst"},
    {"name": "Accenture India", "portal_type": "Workday", "job_id": "BLR-JOB-001", "role": "Global Business Operations & BD Analyst"},
    {"name": "Goldman Sachs India", "portal_type": "Custom Enterprise", "job_id": "Req #181727", "role": "Global Markets Operations Analyst"},
    {"name": "JPMorganChase India", "portal_type": "Taleo / ContactHR", "job_id": "Ref #153450123", "role": "Trade Lifecycle Associate I"},
    {"name": "Swiss Re GBS India", "portal_type": "SuccessFactors", "job_id": "SRE-BLR-OPS-2026", "role": "Operations & Reinsurance Risk Analyst"},
    {"name": "Walmart Global Tech", "portal_type": "Workday", "job_id": "WMT-BLR-OPS-4102", "role": "Supply Chain & Retail Operations Analyst"},
    {"name": "Amazon India", "portal_type": "Amazon Jobs", "job_id": "AMZ-BLR-TRMS-9912", "role": "Operations Specialist (TRMS / SCM)"},
    {"name": "Ernst & Young (EY GDS)", "portal_type": "SuccessFactors", "job_id": "BLR-JOB-003", "role": "Business Analyst - Global Advisory"},
    {"name": "KPMG Global Services", "portal_type": "Workday", "job_id": "KGS-BLR-MT-2026", "role": "Global Risk & Management Trainee"},
    {"name": "PwC Service Delivery Center", "portal_type": "Workday", "job_id": "PWC-BLR-OPS-3301", "role": "Business Operations Analyst"},
    {"name": "IBM India", "portal_type": "Kenexa / BrassRing", "job_id": "BLR-JOB-009", "role": "Supply Chain & Operations Consultant"},
    {"name": "Airbus India", "portal_type": "Workday", "job_id": "AIR-BLR-AGGP-2026", "role": "Aviation Logistics & SCM Operations Associate"},
    {"name": "Shell Business Operations", "portal_type": "Workday", "job_id": "SBO-BLR-SCM-3190", "role": "Commercial SCM Operations Trainee"},
    {"name": "Target India", "portal_type": "Workday", "job_id": "R0000342918", "role": "Analyst PIM Ops / Demand Planning"},
    {"name": "Dell Technologies", "portal_type": "Workday", "job_id": "DELL-OPS-BLR-5512", "role": "Global Operations Associate (SCM)"},
    {"name": "Cisco Systems", "portal_type": "Workday", "job_id": "CSCO-IND-OPS-7721", "role": "Business Operations & SCM Specialist"},
    {"name": "Standard Chartered GBS", "portal_type": "Taleo", "job_id": "SCB-IN-GBS-44821", "role": "Trade Operations Specialist (LC / EXIM)"},
    {"name": "PhonePe", "portal_type": "Greenhouse", "job_id": "PPE-OPS-BLR-0192", "role": "Business Operations Analyst"},
    {"name": "Razorpay", "portal_type": "Lever", "job_id": "RZP-OPS-2026-F1", "role": "Analyst, Business Operations"},
    {"name": "CRED", "portal_type": "Greenhouse", "job_id": "CRD-OPS-2026-F2", "role": "Founder's Office Associate"},
    {"name": "Zepto", "portal_type": "Lever", "job_id": "ZPT-OPS-2026-F3", "role": "City Operations & Dark Store Turnaround Lead"},
    {"name": "Swiggy", "portal_type": "Greenhouse", "job_id": "SWG-OPS-2026-F4", "role": "Chief of Staff Associate (Instamart)"},
    {"name": "Ather Energy", "portal_type": "SmartRecruiters", "job_id": "ATH-OPS-2026-F5", "role": "Founder's Office - Integrated SCM"},
    {"name": "Groww", "portal_type": "Lever", "job_id": "GRW-OPS-2026-F6", "role": "Trade Operations & Client Onboarding"},
    {"name": "Meesho", "portal_type": "Greenhouse", "job_id": "MSH-OPS-2026-F7", "role": "Category Operations Lead (Valmo Logistics)"},
    {"name": "Delhivery", "portal_type": "Darwinbox", "job_id": "DLH-OPS-2026-F8", "role": "Express Freight & Logistics Executive"},
    {"name": "DHL Express India", "portal_type": "SuccessFactors", "job_id": "DHL-BLR-EXIM-101", "role": "EXIM Freight Operations Associate"},
    {"name": "A.P. Moller - Maersk", "portal_type": "Workday", "job_id": "MSK-BLR-LOG-202", "role": "Ocean Logistics Operations Trainee"},
    {"name": "Schneider Electric", "portal_type": "Taleo", "job_id": "SCH-BLR-SCM-303", "role": "Global Supply Chain Executive"}
]

payloads = []

for company in TARGET_COMPANIES:
    c_name = company["name"]
    role = company["role"]
    c_payload = {
        "company": c_name,
        "portal_type": company["portal_type"],
        "job_id": company["job_id"],
        "target_role": role,
        "candidate": CANDIDATE,
        "custom_questions": {
            "why_company": ESSAY_BANK["why_company"].format(company=c_name),
            "challenge_solved": ESSAY_BANK["biggest_challenge"],
            "conflict_handling": ESSAY_BANK["conflict_resolution"],
            "key_strength": ESSAY_BANK["strength"],
            "career_goals": ESSAY_BANK["future_goals"].format(company=c_name)
        },
        "attachments": {
            "resume_pdf": f"reports/summer_2027_pdf_packages/APX-2027-001_Tesla_Resume.pdf",
            "cover_letter_pdf": f"reports/summer_2027_pdf_packages/APX-2027-001_Tesla_Cover_Letter.pdf"
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    payloads.append(c_payload)

# Save Master JSON
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(payloads, f, indent=2)

# Generate Markdown Dossier
md_content = f"""# ATS AUTO-FILL & COPILOT PRE-FILL MASTER DOSSIER
**Candidate:** Aditya Mehra | BBA International Business (DSU '26) | Bengaluru  
**Generated:** `{datetime.now().strftime('%A, %B %d, %Y')}`  
**Status:** `READY FOR INSTANT AUTOFILL (SIMULATES SIMPLIFY+ / TEAL+)`  

---

## 1. Universal Applicant Profile Fields (Copy-Ready)

| Field Name | Standard Value | ATS Field Match |
| :--- | :--- | :--- |
| **First Name** | `Aditya` | `first_name`, `First`, `FName` |
| **Last Name** | `Mehra` | `last_name`, `Last`, `LName` |
| **Email** | `adityamehra007@gmail.com` | `email`, `EmailAddress` |
| **Phone** | `+91 7003456624` | `phone`, `mobile`, `cell` |
| **Location** | `Bengaluru, Karnataka, India` | `city`, `location`, `address` |
| **Postal Code** | `560068` | `postal_code`, `zip` |
| **LinkedIn** | `https://www.linkedin.com/in/adityamehra` | `linkedin_url`, `social_link` |
| **Work Auth** | `Citizen of India (No Sponsorship Needed)` | `work_authorization`, `visaSponsorship` |
| **Notice Period**| `Immediate / 0 Days (Fresher Cohort '26)` | `notice_period`, `availability` |
| **Expected CTC** | `₹7,50,000 - ₹9,50,000 LPA` | `expected_salary`, `compensation` |

---

## 2. Standard Enterprise Essay Responses (Simplify+ Parity)

### Question 1: "Why do you want to join our organization?"
```text
I have closely tracked [Company]'s operational leadership and technological scale in Bengaluru. With my proven experience coordinating high-stakes ground operations at Aero India 2025, structuring tier-1 vendor rate cards to achieve a 15% cost reduction, and executing multi-modal AI dataset quality at Instawork AI, I am eager to apply this rigorous operational discipline to deliver immediate, measurable value at [Company].
```

### Question 2: "Describe a complex challenge you solved under pressure."
```text
During Aero India 2025 at Yelahanka Air Force Station, a critical tier-1 audio-visual vendor was stalled at the gate due to vehicle pass discrepancies 90 minutes before VIP walkthrough. I decoupled the physical delivery from the commercial dispute: dispatched our liaison with master manifests to Gate 4, authorized manual perimeter unloading to bypass staging bottlenecks, and directed the booth team to configure backup gear. We completed setup at 07:22 AM (8 mins ahead of deadline) with 100% uptime and 0% shrinkage across ₹12.5L inventory.
```

### Question 3: "How do you resolve vendor or stakeholder conflicts?"
```text
When a long-term merchandise supplier issued an uncontracted 12.5% surcharge invoice right before a client activation, I avoided an operational halt by issuing an immediate voucher for the undisputed contracted amount under clause 4.2 of our MSA. Concurrently, I conducted an algorithmic rate card reconciliation proving the price surge was uncontracted. The vendor released goods on time, and we preserved the ₹15,000 margin (11.1% cost avoidance) without damaging the vendor relationship.
```

---

## 3. Top 30 Target Enterprise Auto-Fill Manifests

| # | Company | Portal Type | Target Role | Job ID | Auto-Fill Status |
|---|---|---|---|---|---|
{"".join(f"| {idx+1} | **{p['company']}** | `{p['portal_type']}` | {p['target_role']} | `{p['job_id']}` | `READY_FOR_AUTOFIL` |\\n" for idx, p in enumerate(payloads))}

---
*Generated deterministically by Antigravity Apex Career OS Autofill Engine.*
"""

with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"Generated {len(payloads)} ATS Autofill Payloads.")
print(f"  JSON: {OUT_JSON}")
print(f"  Markdown: {OUT_MD}")
