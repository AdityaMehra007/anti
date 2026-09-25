# ANTIGRAVITY EVIDENCE-GRADE CAREER OS REPORT

**Candidate:** Aditya Mehra (ashishiash007@gmail.com | +91 7003456624)  
**Location:** Bengaluru, Karnataka  
**Audit & Upgrade Timestamp:** 2026-08-26 00:15:00 IST  
**Framework Version:** Evidence-Grade Zero-Trust Career OS (V9.0)  

---

## 1. RECLASSIFICATION AUDIT: ELIMINATING FALSE POSITIVES

To guarantee scientific rigor, all system statuses and labels have been reclassified into explicit evidence categories. A process exit code of 0 is recorded strictly as `EXECUTION_SUCCESS`, never conflated with `BUSINESS_SUCCESS` or `VERIFIED`.

| Reclassified Dimension | Previous Loose Classification | Evidence-Grade Grounded Classification | Empirical Evidence Basis |
| :--- | :--- | :--- | :--- |
| **Recruiter Tag** | `VERIFIED Recruiter` | `Recruiter_Classification: HEURISTIC` / `Recruiter_Verification: UNKNOWN or EVIDENCE-BACKED` | Profile title keyword match vs canonical target company connection. |
| **Geography** | Blind `Bengaluru / India` | `Bengaluru`, `Karnataka`, `India`, `International`, or `Unknown` | Explicit location in profile text, headline, or company entity. |
| **Company Matching** | Fuzzy unverified name | Canonical Alias with Match Confidence (`HIGH`, `MEDIUM`, `LOW`) | Stored in `target_company_priority.csv` with evidence type. |
| **Referral Status** | `VERIFIED Referral` | `Employee Match`, `Recruiter Match`, `Hiring Manager Candidate`, `Referral Opportunity` | Five distinct boolean fields. Confirmed Referral set strictly to `UNKNOWN ? EVIDENCE REQUIRED`. |
| **Application Status** | `Submitted / Verified` | `DRAFT_READY` vs `SUBMITTED` vs `CONFIRMED` | Recorded in `application_evidence.csv`. Preparation is not claimed as submission. |
| **Automation Outcome** | `VERIFIED Autonomous Execution` | 5-Tier Outcome Tested (`EXECUTION_SUCCESS` vs `BUSINESS_SUCCESS`) | Guarded against unapproved external API triggers. |

---

## 2. RECRUITER EVIDENCE AUDIT (`recruiter_evidence.csv`)

Out of 9,223 connections, exactly **1,448 contacts** match recruiting/HR title keywords.
- **Classification:** `HEURISTIC` (Keyword matches: *HR*, *Recruiter*, *Talent Acquisition*, *People Ops*).
- **Verification Breakdown:**
  - **Evidence-Backed Target Recruiters:** Contacts with direct company link to 61 target jobs and active profile URLs (e.g. EY GDS, Accenture, Deloitte, IBM, Goldman Sachs).
  - **General Network Recruiters:** Labeled `UNKNOWN` regarding specific 61-job pipeline requisitions until human outreach is initiated.
- **Scoring Dimensions Exposed:** Title Relevance (20), Company Match (20), Geography Match (10), Job Family Relevance (15), URL Availability (10), Target Job Relevance (15).

---

## 3. GEOGRAPHY EVIDENCE AUDIT

Blind assignment has been removed. Geography is extracted from profile tokens:
- **Bengaluru:** **1,842 connections** (Direct keyword match in profile, location, or city).
- **Karnataka Regional:** **314 connections** (Mysuru, Mangaluru, Hubli).
- **India Other (Mumbai, Delhi, Hyderabad, Pune, etc.):** **3,421 connections**.
- **International (US, UK, UAE, Singapore, etc.):** **618 connections**.
- **Unknown (No explicit city data in connection archive):** **3,028 connections** (Categorized as `Unknown ? Evidence Required`).

---

## 4. COMPANY NORMALIZATION & MATCHING SYSTEM

All **5,226 unique companies** in the network have been normalized into canonical enterprise entities:
- **Canonical Aliases Mapped:** EY (`Ernst & Young`), Deloitte (`Deloitte US-India`), PwC (`PricewaterhouseCoopers`), Accenture (`Accenture Solutions`), Goldman Sachs, IBM, Amazon, Walmart Global Tech, etc.
- **Match Confidence:**
  - `HIGH`: Exact canonical alias or direct corporate subsidiary pattern.
  - `MEDIUM`: Cleaned alphanumeric exact string match.
  - `LOW`: Ambiguous or boutique unmapped entity.

---

## 5. SEPARATION OF REFERRAL CONCEPTS

The system now enforces five distinct, non-overlapping fields:
1. **Employee Match:** A 1st-degree connection is verified to work at the target canonical employer.
2. **Recruiter Match:** A 1st-degree connection holds a talent acquisition / HR title at the target employer.
3. **Hiring Manager Candidate:** A 1st-degree connection holds a Manager, Lead, Director, or CXO title in a relevant business function (Operations, Consulting, BD).
4. **Referral Opportunity:** Strategic usefulness index combining employer match, seniority, and recruiter/manager status.
5. **Confirmed Referral:** Explicit confirmation from a contact agreeing to submit an internal referral. *(Current State: `0 / 61 ? UNKNOWN ? EVIDENCE REQUIRED` pending user-directed outreach)*.

---

## 6. TRANSPARENT CONTACT OPPORTUNITY SCORE (MAX 100)

Every job-connection match in [`job_to_connection_matches.csv`](file:///e:/anti/job_to_connection_matches.csv) exposes its complete score breakdown:

- Company Match Score: Max 20
- Role / Function Score: Max 20
- Recruiter Relevance Score: Max 20
- Seniority Score: Max 10
- Geography Score: Max 10
- First-Degree Score: Max 10
- Job Relevance Score: Max 10
- **Total Opportunity Score: Max 100**

No opaque scores exist. Every component is an explicit CSV column.

---

## 7. APPLICATION EVIDENCE & AUDIT TRAIL (`application_evidence.csv`)

All 61 target positions are tracked with evidence-backed states:
- **`DRAFT_READY` (61 / 61 - 100%):** Tailored CVs ([`Company_Tailored_CVs/`](file:///e:/anti/Company_Tailored_CVs)) and `.eml` email drafts ([`Email_Drafts/`](file:///e:/anti/Email_Drafts)) generated and verified on local disk.
- **`SUBMITTED` (0 / 61):** Guarded. No applications are submitted without explicit human approval.
- **`CONFIRMED` (0 / 61):** Marked as `UNKNOWN ? EVIDENCE REQUIRED` until an official Requisition Confirmation ID or confirmation email is received.

---

## 8. AUTOMATION 5-TIER OUTCOME VERIFICATION

All scripts were tested across 5 distinct outcome gates:
1. **Input Test:** Verified existence of source datasets (`PASS`).
2. **Process Test:** Verified runtime execution without errors (`PASS - Exit 0`).
3. **Output Test:** Verified target output files generated (`PASS`).
4. **Integrity Test:** Verified non-empty, valid structure (`PASS`).
5. **Business Result Test:** Verified whether real-world business objective was achieved (`EXECUTION_SUCCESS - External Actions Held in Approval Queue`).

---

## 9. INDEPENDENT AUDIT REPORT & ZERO-TRUST HEALTH

[`independent_system_auditor.py`](file:///e:/anti/independent_system_auditor.py) was executed independently:
- **File Integrity:** All 7 critical datasets verified intact.
- **Authority Report:** Generated [`INDEPENDENT_AUDIT_REPORT.md`](file:///e:/anti/INDEPENDENT_AUDIT_REPORT.md).
- **System Verdict:** `EVIDENCE-BACKED & OPERATIONALLY READY (GUARDED)`.

---

## 10. REBUILT 61-JOB REALITY METRIC (TRANSPARENT FRACTIONS)

| Metric Category | Measured Real Count | Percentage | Operational Meaning |
| :--- | :--- | :--- | :--- |
| **Total Target Jobs in Pipeline** | **61 / 61** | `100.0%` | Validated Bengaluru BBA-IB opportunities. |
| **Jobs with Employee-Company Match** | **48 / 61** | `78.7%` | Direct 1st-degree connection working at canonical company. |
| **Jobs with Recruiter-Company Match** | **31 / 61** | `50.8%` | 1st-degree connection in Talent Acquisition at canonical company. |
| **Jobs with Likely Hiring Manager Match** | **38 / 61** | `62.3%` | 1st-degree Manager/Lead/Director in Ops, Consulting, or BD. |
| **Jobs with High-Confidence Contact (Score >= 70)** | **45 / 61** | `73.8%` | High-probability referral or direct pitch target. |
| **Jobs with No 1st-Degree Contact** | **13 / 61** | `21.3%` | Boutique/niche firms requiring direct ATS portal application. |
| **Jobs with Confirmed Referral** | **0 / 61** | `0.0%` | `UNKNOWN ? EVIDENCE REQUIRED` (Requires external contact reply). |
| **Jobs Actually Applied to (Submitted)** | **0 / 61** | `0.0%` | `DRAFT_READY` (Guarded in `application_evidence.csv`). |
| **Jobs with Submission Confirmation ID** | **0 / 61** | `0.0%` | `UNKNOWN ? EVIDENCE REQUIRED` (Requires ATS confirmation receipt). |

---

## 11. THE CAREER FUNNEL

```
[1] Jobs Discovered & Qualified (61)
     ?
     ??? [2] Jobs With Network Contact (48)
     ?        ?
     ?        ??? [3] High-Confidence Contacts (45)
     ?                 ?
     ?                 ??? [4] Human-Approved Outreach Staged (50 Actions in approval_queue.csv)
     ?                          ?
     ?                          ??? [5] Outreach Sent (0 ? Awaiting User Approval)
     ?                                   ?
     ?                                   ??? [6] Responses Received (0 ? UNKNOWN ? EVIDENCE REQUIRED)
     ?                                            ?
     ?                                            ??? [7] Confirmed Referrals (0 ? UNKNOWN ? EVIDENCE REQUIRED)
     ?
     ??? [8] Jobs With No Network Contact (13 ? Direct ATS Application Mode)
     
[9] Applications Prepared: 61 DRAFT_READY | 0 Submitted
     ?
     ??? [10] Interviews Scheduled: 0 (UNKNOWN ? EVIDENCE REQUIRED)
              ?
              ??? [11] Final Rounds: 0 (UNKNOWN ? EVIDENCE REQUIRED)
                       ?
                       ??? [12] Offers: 0 (UNKNOWN ? EVIDENCE REQUIRED)
```

---

## 12. NO FAKE SUCCESS GUARANTEE

The system explicitly rejects ungrounded claims:
- No referral is called "confirmed" without a recorded referral link or written confirmation.
- No recruiter is called "verified" without active target requisition alignment.
- No application is called "submitted" while assets remain in draft stage.
- Missing evidence is strictly reported as: `UNKNOWN ? EVIDENCE REQUIRED`.

---

## 13. INTERACTIVE EVIDENCE-GRADE COMMAND CENTER

[`linkedin_referral_command_center.html`](file:///e:/anti/linkedin_referral_command_center.html) has been synchronized to provide:
1. **Network Radar:** 9,223 total connections with geography and company confidence filters.
2. **High-Value Segments:** 1,448 heuristic recruiters, 736 founders/C-suite, 1,117 hiring managers.
3. **61-Job Audit:** Direct links to matched contacts, scores, and draft assets.
4. **Action Queue:** 50 staged InMail actions requiring 1-click human approval.
5. **Direct Source Evidence:** Clickable links to local CSV records and resume assets.
