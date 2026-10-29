## 2026-10-24T17:42:45Z
You are Worker 3 (Approval Queue Sync Worker).
Read the authoritative request at: `e:\anti\.agents\teamwork\ORIGINAL_REQUEST.md`
Read Explorer 1 handoff at: `e:\anti\.agents\teamwork\explorer_survey_1\handoff.md` (Section 1.4 Approval Queue Canonical Schema)
Read `data/approval_queue.csv` and `data/approval_queue.json`
Read updated dockets at `teamwork_projects/bangalore_referral_strike/bangalore_live_referral_dockets.json`

Your working directory is: `e:\anti\.agents\teamwork\worker_queue_1`
Maintain your `progress.md` and write your complete report to `e:\anti\.agents\teamwork\worker_queue_1\handoff.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A reviewer and auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your exclusive write ownership:
- `data/approval_queue.csv`
- `data/approval_queue.json`
- `scripts/sync_referral_to_approval_queue.py` (or synchronization script)

Your mission:
Sync all generated P0/P1 referral actions into `data/approval_queue.csv` and `data/approval_queue.json` without breaking existing schemas (R4):
1. Schema Fidelity:
   Both CSV and JSON must maintain the exact 14 standard columns:
   `Action ID`, `Person`, `Company`, `Job`, `Channel`, `Draft Message`, `Reason / Evidence`, `Priority`, `Approval Required`, `Status`, `Staged Timestamp`, `Approved Timestamp`, `Dispatched Timestamp`, `Dispatch Packet`.
2. Target Staging:
   - For all verified contacts of the 11 target employers (especially including the newly added PwC contacts: Shalini Jha, Nikhitha Simon, Latha Dhananjay, Neeraja Rajasekar, Mishfa Kazi), stage referral outreach actions.
   - Channel: `LinkedIn Employee Referral` (for employee/manager contacts) or `LinkedIn Recruiter InMail` (for recruiter contacts).
   - Priority: `P0 - Bangalore Live Opening`.
   - Approval Required: `'TRUE'`.
   - Status: `'STAGED_READY'`.
   - Reason / Evidence: `Bengaluru Tech Corridor: {corridor} | Verified Profile Match | LinkedIn Referral Target`.
   - Dispatch Packet: JSON string with `linkedin_url`, `connection_note`, `referral_docket`, `job_url`.
3. Deduplication & Sequence:
   - Deduplicate against `(Person, Company, Job)` key so existing actions are not duplicated.
   - Sequence numbering must strictly continue after the maximum existing ID (currently `REF-0604` -> start at `REF-0605` onwards).
   - Row parity: `len(approval_queue.csv) == len(approval_queue.json)`.
4. Verification:
   Run `python -m unittest -v tests/test_bangalore_referral_strike.py` (specifically verifying `test_08_approval_queue_schema_fidelity`).
