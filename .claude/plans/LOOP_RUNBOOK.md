# OMEGA Autonomous Loop Runbook

**Pattern**: `infinite`  
**Mode**: `safe` (Strict Quality Gates & Cryptographic Verification)  
**Branch Strategy**: `master` (Monitored Sovereign Trunk)  
**Model Tier Strategy**: `inherit` / `pro` (High-Reasoning Governance) + Local Async Substrates  

---

## 1. Loop Architecture & Operating Cadence

```
+-------------------------------------------------------------+
|                OMEGA Supervisor Daemon (:8095)              |
|                                                             |
|   [Service 1] aios_gateway (:8090)                          |
|   [Service 2] tradenexus_api (:8000)                        |
|   [Service 3] plane_webhook_reactor (:8092)                 |
|   [Service 4] automation_scheduler (Interval: 30s)          |
|                 └── Auto-Apply Trigger (Cadence: >= 60s)    |
|   [Service 5] live_telemetry_relay (:8096)                  |
|   [Service 6] plane_autonomous_worker (Task Queue)          |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                Periodic Constitutional Cycle                |
|                                                             |
|   1. Auto-Apply Batch Processing (Global 10,000 Pool)       |
|   2. SHA-256 Ledger Block Reconciliation                    |
|   3. 24-Agent Sovereign Fleet & 12-Department Swarm         |
|   4. Master Bundle Recompilation (.ZIP + Portals)           |
|   5. Automated Pytest Verification Gateway                  |
+-------------------------------------------------------------+
```

---

## 2. Safety Gates & Verification Criteria

Before each loop iteration and after every batch expansion:
- **Zero Vibe Coding Gateway**: Run `pytest -q tests/test_interview_cockpit.py tests/test_career_command_center.py tests/test_auto_apply_pipeline.py`.
- **SHA-256 Chain Audit**: Run `python omega_cli.py ledger-verify` to ensure 100% block integrity.
- **Candidate Ground Truth Preservation**: Strictly preserve Aditya Mehra's verified credentials (BBA International Business DSU '26 | AERO India 2025 Coordinator | Instawork AI Data Ops 99.2% QA Precision). Zero invented CGPA or telecalling roles.
- **Deduplication Invariant**: Strict unique constraint on `target_id` and `contact_email` across `data/outreach_tracker.db`.

---

## 3. Explicit Stop Conditions

The autonomous loop halts immediately if any of the following occur:
1. **Target Pool Exhaustion**: All 10,000 Global Requisitions have reached `AUTO_APPLIED_PACKET_STAGED` status.
2. **User Abort**: Explicit `/loop-stop` or `/goal-cancel` command from user.
3. **Safety Gate Breach**: Any unit test failure in the core test suites.
4. **Port Collision or Deadlock**: Supervisor heartbeat fails for >3 consecutive polling cycles (90s).

---

## 4. Monitoring & Operator Commands

### Health & Telemetry
```powershell
# 1. Check live supervisor daemon status
curl http://localhost:8095/status

# 2. Check total auto-applied applications count
python -c "import sqlite3; conn = sqlite3.connect('data/outreach_tracker.db'); print('Total:', conn.execute('SELECT COUNT(*) FROM automated_applications').fetchone()[0])"

# 3. Verify SHA-256 ledger integrity
python omega_cli.py ledger-verify

# 4. View interactive Career Command Center
Start-Process "apps/job_application_studio/career_command_center.html"
```

### Manual Trigger & Bundle Compilation
```powershell
# Run manual batch of 100 targets
python scripts/auto_apply_job_pipeline.py --batch 100

# Recompile master export archive
python scripts/download_all_applications_bundle.py

# Run all 13 constitutional modes
python omega_cli.py do-everything
```
