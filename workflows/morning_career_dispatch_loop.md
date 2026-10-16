# WORKFLOW SPECIFICATION: Morning Career Dispatch & Follow-Up Loop
**File**: `workflows/morning_career_dispatch_loop.md`  
**Domain**: Career Operations & Application Pipeline  
**Status**: APPROVED & SPECIFIED (Definition of Done Met)  
**Implementation Seam**: `e:/anti/AI-Command-Center/automation/daily_career_briefing.py` & `e:/anti/AI-Command-Center/run_command_center.py`

---

## 1. Loop Profile & Overview
- **Objective**: Deliver a zero-friction, decision-ready weekday morning application pipeline for Aditya Mehra targeting entry-level, non-sales Business Operations, SCM, and Operations Analyst positions across Bengaluru corporate hubs.
- **Duration**: Total daily human interaction $< 15$ minutes.
- **Ground Truth**: Strictly grounded in Aditya Mehra's verified credentials (BBA International Business DSU '26, 300+ events, AERO India 2025, Instawork AI data ops 99%+ QA, Pencil Mark written commendation).
- **Core Storage**: `AI-Command-Center/projects/flagship-career-engine/career_vault.db` (`jobs` and `applications` tables).
- **Output Brief**: `AI-Command-Center/DAILY_BRIEFING.md` & Web Cockpit (`index.html`).

---

## 2. Trigger
- **Mechanism**: Hybrid Event + Schedule Trigger.
- **Triggers**:
  1. *Windows Startup/Unlock Event*: Launched via Windows Task Scheduler or Startup Shortcut pointing to `RUN_DAILY_BRIEFING.bat`.
  2. *On-Demand User Trigger*: Execution of `START_FULL_CYCLE.bat` or `RUN_DAILY_BRIEFING.bat`.
  3. *Cron Schedule*: Monday–Friday at 08:30 AM IST.
- **Pre-Conditions**:
  - `career_vault.db` must exist and be accessible.
  - No network connectivity required for vault scoring, document assembly, or brief rendering (100% offline-first).

---

## 3. Autonomous Execution Pipeline (Pre-Checkpoint)

All steps run fully autonomously with zero human prompts:

1. **Vault Scoring & Triage Query**:
   - Query `jobs` table ordered by `fit_score DESC, created_at DESC`.
   - Filter for `status = 'NEW'` or `status = 'DISCOVERED'`.
   - Select top 3 highest-scoring non-disqualified roles ($\text{Score} \ge 80$).
2. **Follow-Up Cadence Audit**:
   - Query `applications` table where `follow_up_date <= DATE('now')` and `outreach_status != 'FOLLOWED_UP'`.
   - If records exist, compile Day-3/Day-7 recruiter follow-up notices into the queue.
3. **Application Asset Assembly**:
   - Verify presence of dual-format resumes:
     - Master ATS (`ADITYA_MEHRA_MASTER_ATS_RESUME.pdf` & `.docx`)
     - Supply Chain & Procurement (`ADITYA_MEHRA_SUPPLY_CHAIN_PROCUREMENT.pdf` & `.docx`)
     - AI & Data Operations (`ADITYA_MEHRA_AI_DATA_OPERATIONS.pdf` & `.docx`)
   - Cross-check `asset_index.json` to link pre-drafted cover letters (`cover_letters/`) and `.eml` drafts (`Email_Drafts/`).
4. **Brief Synthesis & Dashboard Recompile**:
   - Generate `DAILY_BRIEFING.md` formatted with top 3 priority roles, portal links, and the STAR Interview Question of the Day.
   - Recompile `index.html` with current application statuses.
5. **Vault State Preservation**:
   - Execute timestamped snapshot backup to `backups/career_vault_YYYYMMDD_HHMMSS.db`.

---

## 4. Checkpoint (Push-Right)

The checkpoint is pushed to the terminal edge of the pipeline. The human is never asked to choose companies, format text, or search folders.

### The Decision-Ready Brief
- **Surface**: `DAILY_BRIEFING.md` and Local Web Cockpit (`http://localhost:8080/projects/flagship-career-engine/` or `index.html`).
- **Brief Contents**:
  - **Requisition Header**: Company name, exact role title, requisition ID, physical location hub (e.g. Manyata Tech Park, Hebbal), and fit score (e.g. 91/100).
  - **One-Click Portal Link**: Direct URL to workday or career portal.
  - **One-Click Outreach Snippet**: Pre-filled, personalized recruiter InMail text with phone, email, and live portfolio URLs.
  - **Pre-Linked Documents**: Matched ATS PDF resume and tailored cover letter download buttons.
  - **Due Follow-Ups**: Clear checklist items for any applications submitted 3+ days prior.

### Human Action
1. Review brief (60 seconds).
2. Click direct portal link to submit the pre-staged ATS PDF resume.
3. Click "Copy Outreach" to send in-house recruiter LinkedIn message.
4. Select `Applied` in the dashboard status dropdown (commits to `localStorage` and `career_vault.db`).

---

## 5. Failure Modes & Edge Case Recovery

| Failure Mode | Autonomous Handling | Fallback |
| :--- | :--- | :--- |
| **Zero New Roles $\ge 80$** | Expand query to roles with $\text{Score} \ge 70$. | Brief notes: *"Top Tier targets exhausted. Showing 3 high-potential Tier-2 tracks."* |
| **Word COM Unavailable** | Skip `.docx` to `.pdf` re-conversion; rely on pre-compiled `.pdf` files. | Log non-fatal warning; proceed with brief. |
| **Database Lock / Busy** | SQLite timeout configured to 5000ms with WAL mode retry. | Abort snapshot backup; do not corrupt primary vault. |
| **No Internet Connection** | Entire pipeline executes offline using cached SQLite records. | Portal submission deferred until connectivity resumes. |

---

## 6. Definition of Done & Verification Criteria
- [x] Executable script in place: `automation/daily_career_briefing.py` generates compliant brief in $< 1.5$ seconds.
- [x] Relational database persistence: `career_vault.db` records jobs, scores, and application dates.
- [x] Dual-format documents verified: PDF and Word resumes tested and verified on disk.
- [x] Automated test coverage: Validated under `TC-10` and `TC-11` in `tests/test_career_engine.py`.
- [x] No questions remaining: Any autonomous implementer can execute and maintain this loop.
