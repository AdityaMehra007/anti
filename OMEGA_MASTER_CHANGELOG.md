# OMEGA MASTER CHANGELOG

### [v26.2.0] - 2026-08-26 (Live Discovery & ULTRA Architecture)
- **Added**: `live_job_discovery.py` connecting directly to live public career APIs.
- **Added**: 4 new SQLite tables in `omega_master.db`: `job_sources`, `job_evidence`, `job_changes`, `job_runs`.
- **Added**: `test_live_job_discovery.py` verifying seed isolation and evidence hashing (50/50 tests passing).
- **Added**: CLI commands `omega live-scan` and `omega top-jobs`.

### [v26.1.0] - 2026-08-26 (Reality Audit & Grounding)
- **Audited**: Independently probed all initial 20 job URLs with live HTTP requests.
- **Fixed**: Downgraded test fixture submission `APP-JOB-AMZN-001` to `READY`.
- **Fixed**: Isolated seeded template jobs as `SEEDED_NOT_VERIFIED` to prevent pipeline pollution.
- **Added**: `test_reality_audit.py` with 6 invariant tests.

### [v26.0.0] - 2026-08-26 (Career War Room & Multi-Model Fabric)
- **Added**: Full 15-module Career War Room in `omega/career_war_room/`.
- **Added**: Local Ollama inference integration (`llama3:latest` on port 11434).
- **Added**: Disaster recovery backup engine with SHA-256 snapshot verification.
