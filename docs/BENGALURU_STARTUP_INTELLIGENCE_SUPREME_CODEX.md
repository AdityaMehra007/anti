# BENGALURU STARTUP INTELLIGENCE & CAREER RADAR SUPREME CODEX
**Codename:** `OMEGA-BANGALORE-STARTUP-INTELLIGENCE-SUPREME`  
**Edition:** Sovereign Autonomous Enterprise Architecture (Version 2.0)  
**Candidate Ground Truth:** Aditya Mehra | BBA International Business (DSU '26, CGPA: 6.33)  
**Location:** Bengaluru, Karnataka, India  
**Date:** 2026-11-03  

---

## 1. System Origin & Supreme Purpose

This ecosystem originated from the foundational directive established in the ChatGPT session ([`chatgpt.com/share/6ae977d2-7e60-83e8-bce9-49ec9a6409f8`](https://chatgpt.com/share/6ae977d2-7e60-83e8-bce9-49ec9a6409f8)):
> *"Create the biggest and the most powerful prompt and give me the list of all the startups in Bangalore... from the past, present, future on an everything and which role I can apply and where is the hiring going on and about that startup and all the job description salary CTC... create the complete database with all the news and everything with the complete timeline everyday..."*

Where ChatGPT hit conversational and token boundaries, this repository fulfills the complete promise by fusing:
1. **The 33,982 Startup India / Karnataka Registry Baseline** (with DPIIT recognition flags).
2. **The Bangalore Top 500 Curated Tech Unicorns & Scaleups** (`raw_startups.py`).
3. **The 5,000 Verified Bengaluru Corporate & Tech Employers Directory** (`BANGALORE_5000_COMPANIES_WEBSITES_CAREERS_MASTER.csv`).
4. **The 75 Live Tracked Non-Sales Positions** (`JOB-001` to `JOB-078`) audited across Wellfound, LinkedIn, and official career portals.
5. **The 16 Verified Institutional Funding Events** (`FUND-002` to `FUND-017`, including C-CAMP ₹500 Cr RDI fund and Credfix ₹16.1 Cr seed).
6. **The 234 Chronological Change Log Delta Events** (`DELTA-20261012` through `DELTA-20261103`).
7. **The 4 Bespoke Staged Application Dossiers** with ATS resumes, cover letters, STAR defense, 30-60-90 day plans, and compensation negotiation scripts.

---

## 2. Candidate Iron Wall Policy

All autonomous discovery, screening, and scoring algorithms strictly enforce the candidate constraint:
* **Target Candidate:** Aditya Mehra (BBA International Business fresher, Class of 2026, Dayananda Sagar University, Bengaluru).
* **Strict Iron Wall (100% Non-Sales):**
  * **PROHIBITED:** Outbound telecalling, B2C cold-calling, field sales, merchant onboarding, insurance lead generation, debt recovery.
  * **PRIORITIZED:**
    1. **Founder's Office Intern / Associate:** Strategic research, executive dashboarding, milestone governance, decision memos.
    2. **Business Operations (BizOps):** Cross-functional scheduling, SOP formulation, metric reconciliation, vendor coordination.
    3. **Global Sourcing & Supply Chain Operations:** Cross-border trade documentation, customs workflows, freight dispatch, vendor SLA audits.
    4. **Enterprise SaaS Customer Success (Non-Sales):** Platform configuration, attendee portal triage, NPS reporting, client health monitoring.
    5. **AI-Enabled Business Process Automation:** Workflow chaining, prompt operations, LLM dashboarding.

---

## 3. Database Architecture & Relational Schemas

**Primary SQLite Vault:** [`bangalore-intelligence/BENGALURU_SUPREME_STARTUP_UNIVERSE.sqlite`](../bangalore-intelligence/BENGALURU_SUPREME_STARTUP_UNIVERSE.sqlite)

### Table 1: `startups_500` (Top 500 Bangalore Tech Companies)
* `id` (INTEGER PRIMARY KEY)
* `name` (TEXT UNIQUE)
* `category` (TEXT)
* `corridor` (TEXT - Bellandur, Koramangala, Indiranagar, Whitefield, Electronic City, etc.)
* `stage` (TEXT - Decacorn, Unicorn, Series C/B/A, Seed)
* `valuation` (TEXT)
* `founded_year` (INTEGER)
* `description` (TEXT)

### Table 2: `companies_5000` (Bengaluru Employers Directory)
* `company_id` (TEXT PRIMARY KEY - `BLR-0001` through `BLR-5000`)
* `company_name` (TEXT)
* `website` (TEXT)
* `careers_url` (TEXT)
* `industry_sector` (TEXT)
* `corridor_tech_park` (TEXT)
* `hr_lead` (TEXT)
* `hr_email` (TEXT)
* `recruitment_desk_email` (TEXT)
* `phone` (TEXT)
* `target_alignment` (TEXT)
* `verification_status` (TEXT)

### Table 3: `live_jobs` (Tracked Startup Opportunities)
* `job_id` (TEXT PRIMARY KEY - `JOB-001` to `JOB-078`)
* `company` (TEXT)
* `title` (TEXT)
* `fit_score` (TEXT - 90%+ for top priority leads)
* `compensation` (TEXT - Exact verified amounts, e.g. ₹20,000–₹30,000/mo, ₹1.2L–₹1.8L)
* `status` (TEXT - `Active`, `Conditional`, `Closed`, `Unverified / Stale`)
* `url` (TEXT - Direct Wellfound / LinkedIn / Portal URL)
* `audit_notes` (TEXT)

### Table 4: `funding_intelligence` (Institutional Rounds)
* `funding_id` (TEXT PRIMARY KEY - `FUND-002` to `FUND-017`)
* `title` (TEXT)
* `amount` (TEXT)
* `details` (TEXT)

### Table 5: `audit_changelog` (Continuous Event Ledger)
* `change_id` (TEXT)
* `change_type` (TEXT - `ACTIVE`, `CONDITIONAL`, `STALE`, `CLOSED`, `NEW`)
* `target` (TEXT)
* `description` (TEXT)

---

## 4. Master 12-Phase Sovereign Lifecycle Manifest

Documented in [`omega/data/bengaluru_startup_intelligence_manifest.json`](../omega/data/bengaluru_startup_intelligence_manifest.json):

1. **Phase 01 (Discovery):** Scoped the complete Bengaluru startup ecosystem across 33,982 DPIIT registrations, 5,000 corporate hubs, and 500 venture-backed scaleups.
2. **Phase 02 (Research):** Audited 75 live vacancies on Wellfound and LinkedIn with zero-guesswork compensation recording.
3. **Phase 03 (Strategy):** Executed algorithmic fit scoring prioritizing Founder's Office (Zethic 97/100, Vantrix 91/100) and Global Sourcing (Y-Not 98/100).
4. **Phase 04 (Build):** Architected the unified SQLite database, master JSON/CSV registries, and interactive mission control cockpit.
5. **Phase 05 (Automation):** Built automated briefing and changelog tracking modules.
6. **Phase 06 (Execution):** Staged 4 submission-ready dossiers into `data/approval_queue.csv`.
7. **Phase 07 (Audit):** Filtered out 4 closed/expired listings (College Circle AI, CrewUP, FirstClub, BiteSpeed) and 7 conditional roles (Finifi, Procureyard).
8. **Phase 08 (Red Team):** Rigorously blocked all tele-sales, cold outbound, and commission-only roles.
9. **Phase 09 (Optimization):** Engineered Google X-Y-Z bullet points grounded in Aero India 2025 VIP ground triage and Puma/Tata Comm brand ops.
10. **Phase 10 (Scale):** Embedded the dashboard into `OMNI_EXECUTIVE_COCKPIT.html`.
11. **Phase 11 (Monitor):** Daily briefing archives established in `bangalore-intelligence/briefings/`.
12. **Phase 12 (Learning):** Codified executable instructions into `START_BENGALURU_STARTUP_INTELLIGENCE.bat` and CLI runner.

---

## 5. One-Click Command Center

* **To launch the full visual cockpit:** Double-click [`START_BENGALURU_STARTUP_INTELLIGENCE.bat`](../START_BENGALURU_STARTUP_INTELLIGENCE.bat).
* **To run the autonomous master engine via CLI:**
  ```powershell
  python e:\anti\bangalore_intelligence_master_engine.py --do-everything
  ```
* **To view the Meta-Cockpit:** Open [`OMNI_EXECUTIVE_COCKPIT.html`](../OMNI_EXECUTIVE_COCKPIT.html) and toggle the **Bengaluru Startup Intelligence & Career Radar** tab.
