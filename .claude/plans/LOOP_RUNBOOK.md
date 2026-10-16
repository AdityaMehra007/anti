# OMEGA Autonomous Loop Runbook

**Pattern**: `sequential` / `infinite` (Autonomous Multi-Cadence Sovereign Pulse)  
**Mode**: `safe` (Strict Quality Gates & Cryptographic Verification)  
**Branch Strategy**: `master` (Monitored Sovereign Trunk)  
**Model Tier Strategy**: `inherit` / `pro` (High-Reasoning Governance) + Local Async Substrates  
**Hook Profile**: `ECC_HOOK_PROFILE=safe` (All validation hooks enforced)  
**Last Verified Baseline**: 395/395 Tests Passed (100% Pass Rate in 139s)

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
|   [Service 7] hermes_autonomous_controller (:9119)          |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                Periodic Constitutional Cycle                |
|                                                             |
|   1. Realtime Hot-Folder Audits & Merkle Block Verification |
|   2. Hourly B2B Industrial Prospecting & Target Scoring     |
|   3. Daily 13-Mode "DO EVERYTHING" & 24-Agent Fleet Cycle   |
|   4. Weekly Valuation Compounding & Mode L Skill Distill    |
|   5. Automated Pytest Verification Gateway                  |
+-------------------------------------------------------------+
```

---

## 2. Safety Gates & Verification Criteria

Before each loop iteration and after every batch execution:
- **Zero Vibe Coding Gateway**: Full unit and integration test coverage (`pytest -q` or `python test_ai_career_os_universal.py`).
- **Cryptographic Merkle Audit**: `python omega_cli.py ledger-verify` to ensure 100% block integrity.
- **Candidate Ground Truth Preservation**: Strictly preserve Aditya Mehra's verified credentials (`EXP-001` through `EXP-005`: BBA International Business DSU '26 | Aero India 2025 Coordinator | Instawork AI Data Ops 99.2% QA Precision | Track: Operations, Logistics/EXIM, Analytics, AI Ops). Zero invented credentials.
- **Human Approval Gate**: Staged 1-click clipboard dispatch; no unauthorized external network transmissions.

---

## 3. Explicit Stop Conditions

The autonomous loop halts execution immediately if any of the following occur:
1. **Target Pool Exhaustion**: All staged target requisitions have reached terminal dispatch status.
2. **User Abort**: Explicit `/loop-stop`, `/goal-cancel`, or `python omega_cli.py autopilot --stop`.
3. **Safety Gate Breach**: Any unit test failure in the core test suites or database schema mismatch.
4. **Daemon Deadlock / Port Collision**: Supervisor heartbeat fails for >3 consecutive polling cycles (90s).

---

## 4. Loop Start & Monitoring Commands

### Starting the Loop
```powershell
# Start autonomous autopilot in background
python omega_cli.py autopilot --start

# OR run in foreground with real-time log streaming
python omega_cli.py autopilot --foreground

# OR execute a single multi-cadence validation pulse
python omega_cli.py autopilot --once
```

### Monitoring the Loop
```powershell
# 1. Check live autopilot status & telemetry
python omega_cli.py autopilot --status

# 2. Check Hermes controller web UI (Port 9119)
curl -s http://127.0.0.1:9119/

# 3. View live generated daily brief
Get-Content E:\anti\DAILY_SOVEREIGN_BRIEF.md -Head 25
```

### Stopping the Loop
```powershell
# Gracefully terminate the autonomous autopilot
python omega_cli.py autopilot --stop
```
