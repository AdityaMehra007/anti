# CAREER HQ — AUTOMATION MAP

| Automation Process | Script / Engine Path | Trigger & Cadence | Output / Log Target | Human Gate | Status |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **Live Job Discovery Scan** | `omega/career_war_room/live_job_discovery.py` | CLI `omega live-scan` / Daily | `omega_master.db` & `automation_runs.jsonl` | None (Read-Only) | **ACTIVE** |
| **Reality Audit & Verifier** | `omega/career_war_room/job_truth_auditor.py` | Periodic / Pre-Brief | `job_evidence` & `truth_events` | None (Audit) | **ACTIVE** |
| **Disaster Recovery Backup** | `omega/engines/disaster_recovery.py` | CLI `omega backup` / On-demand | `omega/data/backups/snapshot_*.tar.gz` | None (Internal) | **ACTIVE** |
| **Application Pre-Filling** | `omega/career_war_room/application_manager.py` | Pipeline Stage Transition | `applications` table | **REQUIRED** | **GATED** |
| **Recruiter Outreach Draft** | `omega/career_war_room/outreach_engine.py` | On New Confirmed Vacancy | `outreach` table | **REQUIRED** | **GATED** |
| **365-Day Scheduled Daemon** | `omega/career_war_room/radar_365.py` | Windows Task Scheduler (08:00 IST)| `automation_runs.jsonl` | None (Monitor) | **CONFIGURED** |
