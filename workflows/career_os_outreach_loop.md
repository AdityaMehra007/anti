# WORKFLOW SPECIFICATION: Autonomous Career OS & Recruiter Outreach Loop
**File**: `workflows/career_os_outreach_loop.md`  
**Domain**: Career OS / Sovereign Operations  
**Status**: APPROVED & ACTIVE  
**Implementation Seam**: `e:/anti/scripts/auto_apply_job_pipeline.py` & `e:/anti/aios/automation/scheduler.py`

---

## 1. Loop Profile & Overview
- **Objective**: Identify qualified global tech and business development requisitions, match against the candidate's verified **Truth Layer** credentials (AERO India 2025, Instawork AI Data Ops 99.2% QA), generate personalized STAR pitch letters, pre-fill zero-password Gmail Compose links and RFC 822 `.eml` dispatches, and record cryptographic SHA-256 audit logs.
- **Cadence**: Continuous minutely loop (automated scheduling via AIOS Scheduler).
- **Target Repository**: `data/global_10000_targets.db`
- **Output Ledger**: `data/outreach_tracker.db` (`automated_applications` and `automated_application_events` tables).

---

## 2. Trigger
- **Primary Mechanism**: Schedule-driven heartbeat.
- **Cadence**: Fires every 60 seconds (`interval_sec = 60`) from `AutomationScheduler.step()`.
- **Condition**: Only selects records where `target_id NOT IN (SELECT target_id FROM automated_applications)` ordered by `fit_score DESC`.

---

## 3. Execution Pipeline (Autonomous Pre-Checkpoint)
1. **Target Identification**:
   - Query target pool with `unapplied_only = True`.
   - Batch size: 5–10 targets per cycle.
2. **Context Tailoring & Truth Verification**:
   - Match candidate profile against `target.job_title`, `target.company`, and `target.corridor`.
   - Construct personalized cover letter and STAR proof matrix referencing verified evidence.
3. **Artifact Generation**:
   - Write structured JSON packet to `applications_generated/auto_applied_packets/{app_id}_{company}.json`.
   - Generate RFC 822 compliant `.eml` draft to `reports/dispatch_queue/{app_id}_{to_email}.eml`.
   - Synthesize direct HTTPS Web Gmail compose link with pre-populated `to`, `subject`, and URI-encoded body.
4. **Cryptographic Proof Stamping**:
   - Compute SHA-256 hash over packet parameters (`proof_hash`).
   - Store record in `automated_applications` with status `AUTO_APPLIED_PACKET_STAGED`.

---

## 4. Checkpoint (Push-Right)
- **Design Rule**: The checkpoint is pushed as far right as possible. All drafting, formatting, email generation, and ledger commits complete autonomously before human interaction.
- **Decision-Ready Brief**:
  - Location: Dashboard Automation table & `reports/dispatch_queue/`.
  - Format: Summary line containing `Company`, `Target Contact`, `Fit Score`, `Subject`, and 1-click Web Gmail link.
  - Human Action: Review brief in 10 seconds -> 1-click open link or trigger batch send.

---

## 5. Verification & Acceptance Criteria
- [x] Zero resource leaks: All SQLite connection handles closed in `try...finally` blocks.
- [x] Deduplication guaranteed: No duplicate application dispatched to the same `target_id`.
- [x] Audit ledger committed: Every staged packet records an immutable row with SHA-256 proof hash in `data/outreach_tracker.db`.
- [x] Gateway and UI integration: Viewable in AIOS Command UI under Automation Status Panel.
