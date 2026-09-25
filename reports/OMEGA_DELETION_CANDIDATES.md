# ANTIGRAVITY OMEGA ULTRA — DELETION & ARCHIVE CANDIDATES

**Document ID:** OMEGA-DELETION-2026-FINAL  
**Standard:** Zero-Risk Staging, Archival First, No Irreversible Destructive Actions  

---

## ⚠️ 1. DELETION & ARCHIVAL POLICY
- **Policy Rule**: Never delete files during an audit phase without an explicit user instruction.
- **Action**: Identify dead, duplicate, stubbed, or superseded files and mark them as candidates for moving to `e:/anti/archive/`.

---

## 🗂️ 2. CANDIDATE CLASSIFICATION

| Target Path | Current Size | Reason for Archival Candidate | Recommended Disposition |
| :--- | :---: | :--- | :--- |
| `e:/anti/artifacts/` | 0 B | Empty legacy directory created in v28. | Safe to delete. |
| `e:/anti/backups/` (Root) | 0 B | Empty legacy backup directory; superseded by `omnivanta/data/backups/`. | Safe to delete. |
| `e:/anti/company/` | 0 B | Empty legacy directory; superseded by `omnivanta/` ontology. | Safe to delete. |
| `e:/anti/customers/` | 0 B | Empty legacy directory; superseded by `omnivanta.db` customers table. | Safe to delete. |
| `e:/anti/datasets/` | 0 B | Empty legacy directory; CSVs reside in root. | Safe to delete. |
| `e:/anti/reports/` (Root) | 0 B | Empty directory; master reports reside in root. | Safe to delete. |
| `e:/anti/test.txt` | 5 B | Scratch temporary text file. | Safe to delete. |
| `e:/anti/run_247_career_loop.py` | 1.4 KB | Superseded by `omnivanta/omega/daily_loop.js`. | Move to `archive/`. |
| `e:/anti/run_all_autopilot.bat` | 2.3 KB | Superseded by unified CLI and `npm start`. | Move to `archive/`. |
| `e:/anti/run_job_apply.js` | 5.7 KB | Superseded by `omnivanta/omega/action_engine.js`. | Move to `archive/`. |
