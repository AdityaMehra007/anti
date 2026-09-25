# CAREER OS v2.0 — SYSTEM INVENTORY & VERIFICATION AUDIT
**Location:** `E:\anti` | **Audit Timestamp:** 2026-08-24 15:08 IST  
**System Status:** V1 Baseline Audited -> Upgrading to **V2.0**

---

## 1. Component Verification & Inventory Matrix

| File / Component Path | Purpose | Dependencies | Inputs / Outputs | Classification Status | Notes & Verification Findings |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `career-hub/candidate/candidate_profile.json` | Master Candidate Identity | None | JSON Data Source | **VERIFIED WORKING** | 100% verified against raw 10-page master CV. |
| `career-hub/candidate/experience_evidence.json` | Work History Evidence Layer | `Master_Resume_Aditya_Mehra_Complete_10_Pages.md` | JSON Data Source | **VERIFIED WORKING** | 9 verified entries with Evidence IDs (`EXP-001` to `EXP-009`). |
| `career-hub/candidate/education.json` | Academic Evidence | Raw Degree Docs | JSON Data Source | **VERIFIED WORKING** | Dayananda Sagar University BBA IB (May 2026). |
| `career-hub/candidate/certifications.json` | Professional Certifications | Certificates | JSON Data Source | **VERIFIED WORKING** | Google, IIT Kharagpur, Outskill, be10x certificates. |
| `career-hub/candidate/career_targets.json` | 5 Ranked Career Tracks | Market Data | Target Track Weights | **VERIFIED WORKING** | Business Dev (95), Ops (94), AI Data Ops (90), EXIM (88), Events (85). |
| `career-hub/candidate/analytics.json` | System Metrics Log | Master CSVs | JSON Logs | **VERIFIED WORKING** | System metrics tracking 4,500+ companies & 61 pipeline. |
| `Master_Resume_Aditya_Mehra_Complete_10_Pages.md` | Untruncated Source Resume | Raw CV PDF | Markdown Document | **VERIFIED WORKING** | Comprehensive 10-page master source document. |
| `Resume_Aditya_Mehra.md` | Master Corporate ATS Resume | Candidate Truth | Markdown Document | **VERIFIED WORKING** | Clean 2-page ATS formatted resume. |
| `Company_Tailored_CVs/*` | 6 Specialized CV Variants | Master Resume | Markdown Resumes | **VERIFIED WORKING** | Tailored CVs for BD, Ops, AI Data, EXIM, Events, Fortune 500, HubSpot. |
| `Interview_Defense_Proof_of_Claims.md` | Q&A Defense Playbook | Candidate Evidence | Markdown Playbook | **VERIFIED WORKING** | 300+ events defense, 15% savings, repeat rate, brand vs payroll. |
| `interview_trainer.html` | Interactive Drill Web App | Playbook | HTML Web App | **VERIFIED WORKING** | Role-specific Q&A drill cards tested in browser. |
| `portfolio/index.html` | Personal Web Portfolio | Candidate Truth | Standalone Web Page | **VERIFIED WORKING** | Sleek dark-mode portfolio showing verified timeline & 300 skills. |
| `index.html` | Master Command Center | All Components | HTML Dashboard | **PARTIALLY WORKING** | Functional dashboard; scheduled for V2.0 upgrade. |
| `bengaluru_job_pipeline.html` | 61-Job Pipeline Web App | Pipeline CSV | HTML Dashboard | **VERIFIED WORKING** | Interactive bar chart & 61 deduplicated jobs. |
| `BBA_IB_Bengaluru_61_Job_Pipeline.csv` | 61-Job Pipeline Dataset | Job Postings | CSV Dataset | **VERIFIED WORKING** | 11 Immediate, 15 Today, 15 Selective, 14 Secondary, 6 Strategic. |
| `Master_4500_Unique_Companies_Deduplicated.csv` | 4,500+ Unique Companies DB | Merged Databases | CSV Dataset | **VERIFIED WORKING** | 100% deduplicated unique company entity records. |
| `master_4500_unique_companies.html` | 4,500 Companies Web App | Deduplicated CSV | HTML Dashboard | **VERIFIED WORKING** | Searchable HTML interface for 4,500+ unique companies. |
| `BBA_International_Business_1400_Companies.xlsx` | User Official Excel DB | User Download | Excel File | **VERIFIED WORKING** | 1,400 companies imported from user's Downloads. |
| `Email_Drafts/*.eml` | 1-Click Email Drafts | Recruiter Scripts | `.eml` Mail Files | **VERIFIED WORKING** | Pre-addressed to Accenture, Deloitte, EY, Amazon, GS, HubSpot. |
| `Recruiter_Outreach_Messages.txt` | LinkedIn Connection Notes | Candidate Evidence | Text Template | **VERIFIED WORKING** | 298-character custom connection notes (under 300 limit). |
| `run_all_autopilot.bat` | Windows Batch Launcher | Windows Shell | Batch Script | **VERIFIED WORKING** | Launches tabs, cover letters, and email drafts on desktop. |
| `run_247_loop.ps1` | Background Logger Script | PowerShell | PowerShell Script | **VERIFIED WORKING** | Tested and executed cleanly via PowerShell. |
| `247_career_loop.log` | Background System Log | PowerShell Logger | Log File | **VERIFIED WORKING** | Real-time logging of background checks. |
| `Scheduled Task (task-308)` | Background Cron Schedule | Schedule Tool | Cron Task | **SCHEDULED AUTONOMOUS**| Fires `0 */4 * * *` (every 4 hours, 24/7). |

---

## 2. Redundancy & Consolidation Strategy
- **Consolidation Target:** Merge duplicate company tracking sheets (`1400_Companies.csv`, `3000_Company_Directory.csv`, `NSE_BSE_MNC.csv`) into the canonical **`Master_4500_Unique_Companies_Deduplicated.csv`**.
- **Dashboard Upgrade:** Upgrade **`index.html`** into the unified V2.0 Operational Command Center with Today, Pipeline, Strategy, System, and Approvals tabs.
