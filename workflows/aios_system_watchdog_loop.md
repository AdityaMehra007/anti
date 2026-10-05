# WORKFLOW SPECIFICATION: AIOS Autonomous System Watchdog & WAL Maintenance
**File**: `workflows/aios_system_watchdog_loop.md`  
**Domain**: Platform & SRE Operations  
**Status**: APPROVED & ACTIVE  
**Implementation Seam**: `e:/anti/aios/automation/scheduler.py` & `e:/anti/aios/scripts/health_check.py`

---

## 1. Loop Profile & Overview
- **Objective**: Continuously collect host machine telemetry (CPU utilization, physical RAM availability, NVIDIA GeForce GTX 960M GPU thermals/VRAM, Drive C: and Drive E: free storage), synchronize metrics into SQLite `system_metrics`, trigger n8n event DAGs, perform passive SQLite WAL checkpoints and query optimizations, and alert on resource degradation.
- **Cadence**:
  - Health Telemetry: Every 300 seconds (5 minutes).
  - SQLite WAL Optimize: Every 3600 seconds (1 hour).
  - Continuous Ledger Integrity: Every 900 seconds (15 minutes).

---

## 2. Trigger
- **Primary Mechanism**: Internal daemon clock in `AutomationScheduler`.
- **Condition**: Time delta comparison against `last_health_sync`, `last_backup`, and `last_audit_sync`.

---

## 3. Execution Pipeline
1. **Host Sensor Probing**:
   - Query `GlobalMemoryStatusEx` via `ctypes.windll.kernel32` for physical RAM.
   - Query `GetDiskFreeSpaceExW` for partition headroom (C: restricted ceiling, E: primary storage).
   - Execute `nvidia-smi` probe for GPU core clock, memory utilization, and thermals.
2. **Telemetry Ingestion**:
   - Insert structured row into `master.db` -> `system_metrics`.
   - Dispatch webhook event to n8n bridge (`run_health_sync_dag`).
3. **Database Maintenance**:
   - Execute `PRAGMA wal_checkpoint(PASSIVE);` to flush write-ahead logs without blocking concurrent readers.
   - Execute `PRAGMA optimize;` to update query planner statistics.
4. **Audit Logging**:
   - Record maintenance operations into `audit_logs` table.

---

## 4. Checkpoint
- **Policy**: Zero Checkpoint (100% Autonomous).
- **Escalation**: Triggers alert brief only if RAM drops below 1.5 GB free or GPU temperature exceeds 82°C.

---

## 5. Verification & Acceptance Criteria
- [x] Tested in `test_automation.py` (`test_04_scheduler_cycle`).
- [x] Zero memory leak background execution.
- [x] Telemetry accessible via Gateway `/api/telemetry` and `/api/recent_metrics`.
