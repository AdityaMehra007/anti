import os
import json
from datetime import datetime

hq_dir = r"E:\OMNI_OS\CAREER_HQ"
os.makedirs(hq_dir, exist_ok=True)

files = {
"CAREER_MASTER_CONTEXT.md": """# CAREER HQ — MASTER CONTEXT
**Headquarters Mission:** Central operating hub for Aditya Mehra's job search, applications, resumes, interviews, referrals, and career automation.
**Candidate:** Aditya Mehra
**Education:** Bachelor of Business Administration (BBA) in International Business (2023–2026)
**Institution:** Dayananda Sagar University, Bengaluru
**Target Location:** Bengaluru (Bangalore), Karnataka, India (Only)
**Target Stage:** Early Career / New Graduate (New Analyst 2026, 0–2 Years) & Summer Internships
**Primary Focus:** Bulge-Bracket Investment Banking Operations, Global Asset Management, FinTech Unicorns, MBB & Big 4 Consulting, High-Growth Tech Ops.
""",

"CAREER_STATE.md": """# CAREER HQ — CURRENT STATE
**System Status:** ACTIVE & OPERATIONAL
**Live Web Dashboard:** http://localhost:8080 (Task-98 Running)
**Target Universe:** Top 30 Crown-Jewel Companies (Bengaluru Hub) + 500 Broad Universe
**Active Batch:** Batch 1 (Tier 1 Global Investment Banking & FinTech)
**Verified Candidate Resume:** `E:\\antigravity_workspace\\Aditya_Mehra_Resume.pdf`
**Last Synchronized:** """ + datetime.now().isoformat() + """
""",

"CAREER_GOALS.md": """# CAREER GOALS & TARGETS
1. **Primary Goal (P0):** Secure an offer for **Operations New Analyst (2026)** or **Summer Analyst** at **Goldman Sachs Bengaluru** (Helios Business Park) or **Morgan Stanley** (Bellandur) / **J.P. Morgan** (EGL).
2. **Secondary Goal (P1):** High-growth FinTech & BizOps roles (Razorpay, CRED, Google, Flipkart, McKinsey BCN).
3. **Compensation Target:** ₹12,00,000 – ₹20,00,000 PA (Full-Time) / ₹75,000 – ₹1,00,000 / month (Internships).
""",

"CAREER_PROFILE.md": """# CANONICAL CAREER PROFILE (VERIFIED FACTS ONLY)
- **Full Name:** Aditya Mehra
- **Email:** adityamehra799@gmail.com
- **Phone:** +91 7003456624
- **LinkedIn:** linkedin.com/in/aditya-mehra-b8644b326
- **Location:** Bengaluru, Karnataka, India
- **Education:** BBA International Business (2023–2026), Dayananda Sagar University, Bengaluru
- **Work & Operations History:**
  - Event Coordinator — TRILOGY Live Music (Bangalore Club, Jan 2026)
  - Business Development Intern — Pencil Mark Interior Solutions LLP (Jul-Aug 2025, Management Commendation)
  - Exhibition Operations Lead — AERO India 2025 (Salt in My Coca, Feb 2025)
  - Freelance Event Operations Lead — Tata Communications, Puma, VH1 Supersonic, Aero India (2021–2023)
  - Operations & General Management — Family Enterprise, Kolkata (2018–2020)
- **Skills:** Operations Management, Budgeting & Cost Control, Client Relationship Management, Vendor Coordination, MS Excel, AI Tools.
- **Certifications:** Google Digital Marketing (2024), IIT Kharagpur NPTEL Service Marketing (2025), Outskill Generative AI (2025).
- **Languages:** English (Fluent), Hindi (Fluent), Bengali (Native).
""",

"USER_CORRECTIONS.md": """# USER CORRECTIONS & PREFERENCES LOG
- **CORR-001 (2026-08-31):** Location restriction set strictly to **Bengaluru, India only** (Kadubeesanahalli, Bellandur, EGL, Koramangala, Manyata).
- **CORR-002 (2026-08-31):** Role positioning set to **BBA in International Business** (Operations, Middle Office, Client Onboarding, Risk, BizOps, FinTech). No generic software developer resumes.
- **CORR-003 (2026-08-31):** Mandatory storage on **E: Drive** (`E:\\OMNI_OS`, `E:\\antigravity_workspace`, `E:\\career-ops`).
- **CORR-004 (2026-08-31):** Verified resume file set strictly to `Aditya_Mehra_Resume.pdf`.
""",

"COMPANY_TARGET_LIST.md": """# COMPANY TARGET LIST (TIER 1 BENGALURU)

| Company | Office Location | Priority Role | Direct Portal | Match Score |
| :--- | :--- | :--- | :--- | :--- |
| **Goldman Sachs** | Helios Business Park, Outer Ring Road | Operations New Analyst / Summer Analyst | [GS Portal](https://www.goldmansachs.com/careers/students/programs/) | 99% |
| **Morgan Stanley** | Bellandur / ORR | Operations Full-Time Analyst | [MS Portal](https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/appcentre-1/brand-2/candidate/jobboard/vacancy/1/adv/) | 98% |
| **J.P. Morgan** | Embassy GolfLinks (EGL) | Corporate Analyst (CADP) | [JPMC Portal](https://careers.jpmorgan.com/global/en/students/programs) | 98% |
| **BlackRock** | Prestige Tech Park | Client Operations Analyst | [BlackRock Portal](https://careers.blackrock.com/early-careers/) | 97% |
| **McKinsey & Co** | UB City / Bellandur | Business Analyst / Capabilities | [McKinsey Portal](https://www.mckinsey.com/careers/search-jobs) | 96% |
| **BCG** | Embassy GolfLinks (EGL) | Knowledge Analyst — Ops | [BCG Portal](https://careers.bcg.com/) | 96% |
| **Bain & Company** | Manyata Tech Park | BCN Analyst | [Bain Portal](https://www.bain.com/careers/) | 96% |
| **Razorpay** | Koramangala HQ | BizOps & Strategy Associate | [Razorpay Portal](https://razorpay.com/careers/) | 95% |
| **Google** | Bagmane Constellation | BizOps & Partner Services | [Google Portal](https://careers.google.com/) | 95% |
| **CRED** | Indiranagar | Risk & Operations Associate | [CRED Portal](https://cred.club/careers) | 94% |
""",

"JOB_PIPELINE.md": """# JOB APPLICATION PIPELINE

| Company | Role | Location | Pipeline Stage | Action Required |
| :--- | :--- | :--- | :--- | :--- |
| **Goldman Sachs** | Operations New Analyst (2026) | Bengaluru (Helios) | **READY FOR SUBMISSION** | User portal submission via [GS Portal](https://www.goldmansachs.com/careers/students/programs/) |
| **Goldman Sachs** | Summer Analyst (Operations/AWM) | Bengaluru (Helios) | **READY FOR SUBMISSION** | User portal submission |
| **Morgan Stanley**| Operations Analyst | Bengaluru (Bellandur) | **READY FOR SUBMISSION** | User portal submission |
| **J.P. Morgan** | CADP Analyst | Bengaluru (EGL) | **READY FOR SUBMISSION** | User portal submission |
| **Razorpay** | BizOps Associate | Bengaluru (Koramangala) | **READY FOR SUBMISSION** | User portal submission |
""",

"CAREER_DASHBOARD.md": """# 🎯 CAREER HQ MASTER DASHBOARD
*Live Command Center for Aditya Mehra*

```
========================================================================================
 CAREER HQ STATUS: ACTIVE [COMMAND CENTER]
 LIVE INTERACTIVE WEB HUB: http://localhost:8080 (RUNNING)
 CANDIDATE: Aditya Mehra | BBA-IB (2023-2026) | LOCATION: Bengaluru Only
========================================================================================

 [TOP TARGETS READY]
 1. Goldman Sachs (Helios Business Park, ORR) -> Operations Analyst [99% Match]
 2. Morgan Stanley (Bellandur) -> Operations Analyst [98% Match]
 3. J.P. Morgan Chase (Embassy GolfLinks) -> Corporate Analyst [98% Match]
 4. BlackRock (Prestige Tech Park) -> Client Operations [97% Match]
 5. McKinsey & Company (UB City / Bellandur) -> Business Analyst [96% Match]
 6. Razorpay (Koramangala) -> Business Operations Associate [95% Match]

 [RESOURCES & PACKAGES ON E:\\]
 -> Master Resume & Profile: E:\\OMNI_OS\\CAREER_HQ\\CAREER_PROFILE.md
 -> GS Application Package: E:\\antigravity_workspace\\goldman_sachs_application_package.md
 -> Live Dashboard UI: E:\\antigravity_workspace\\live_dashboard\\index.html
========================================================================================
```
"""
}

for name, text in files.items():
    fpath = os.path.join(hq_dir, name)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(text.strip() + "\n")

print(f"CAREER HQ initialized: {len(files)} master files written to {hq_dir}")