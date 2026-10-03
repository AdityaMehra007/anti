# 💾 BACKUP STRATEGY & DISASTER RECOVERY: ANTIGRAVITY OMEGA

**Objective**: Guarantee that every critical database, configuration, workflow definition, document, and prompt is rebuildable, verifiable, and protected against data corruption, hardware failure, or human error.  
**Standard**: 3-2-1 Architecture (3 copies, 2 different media, 1 offsite/offdevice).  
**Recovery Target**: RPO < 24 Hours, RTO < 30 Minutes.

---

## 1. Backup Topology Map

```mermaid
flowchart TD
    subgraph LIVE_DATA["Active Production State (E:/anti/aios)"]
        D1["SQLite Databases (*.db)"]
        D2["n8n Workflow Definitions (*.json)"]
        D3["System Configurations & Configs (*.yaml, *.env.example)"]
        D4["Prompt Registry & Research Documents"]
    end

    LIVE_DATA -->|Automated Nightly Snapshot (02:00)| LocalSnap["Tier 1: Local Versioned Snapshot\n(E:/anti/aios/backups/daily_YYYYMMDD.tar.gz)"]
    
    LocalSnap -->|Hourly SQLite VACUUM INTO| WALCopy["Point-in-Time SQLite Cold Copy\n(E:/anti/aios/backups/db/)"]
    
    LocalSnap -->|Cross-Volume Mirror| SecondaryDrive["Tier 2: Secondary Volume Mirror\n(D:/OMEGA_COLD_BACKUP/)"]
    
    LIVE_DATA -->|Encrypted Remote Push| RemoteBackup["Tier 3: Offsite Encrypted Vault\n(Private Git / S3 / Proton Drive)"]
```

---

## 2. Backup Schedules & Retention Policy

| Target Asset | Mechanism | Schedule | Storage Location | Retention |
| :--- | :--- | :--- | :--- | :--- |
| **SQLite Databases** | `VACUUM INTO` / WAL freeze | Daily at 02:00 | `E:\anti\aios\backups\db\` | 30 Days rolling |
| **n8n Workflows** | Git Export / JSON dump | On commit + Daily | `E:\anti\aios\automation\workflows\` | Permanent (Git) |
| **Configurations & Prompts** | Git Version Control | Continuous | `E:\anti\aios\` (Git committed) | Full Git history |
| **Document Vault** | Versioned archive (`tar.gz`) | Weekly | `D:\OMEGA_COLD_BACKUP\` | 8 Weeks |
| **Docker Compose Volumes** | Volume export archive | Bi-weekly | `E:\anti\aios\backups\containers\`| 4 Revisions |

---

## 3. Disaster Recovery Scenarios & Procedures

### Scenario A: SQLite Database Corruption
1. **Diagnosis**: Database returns `SQLITE_CORRUPT` error or queries fail.
2. **Procedure**:
   ```powershell
   # 1. Stop services touching the database
   python e:\anti\aios\scripts\omega_ctl.py stop-core
   
   # 2. Inspect latest backup in backups/db/
   Get-ChildItem e:\anti\aios\backups\db\ -Filter "*.db" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
   
   # 3. Restore snapshot into data directory
   Copy-Item e:\anti\aios\backups\db\master_YYYYMMDD.db e:\anti\aios\data\master.db -Force
   
   # 4. Verify integrity
   python -c "import sqlite3; con = sqlite3.connect('e:/anti/aios/data/master.db'); print(con.execute('PRAGMA integrity_check;').fetchall())"
   
   # 5. Restart services
   python e:\anti\aios\scripts\omega_ctl.py start-core
   ```

### Scenario B: Complete Drive C: Failure or OS Reinstall
1. **Host State**: Windows reinstalled; Drive E: remains intact with all repositories and models.
2. **Procedure**:
   ```powershell
   # 1. Install Git, Python 3.13, uv, Node
   winget install Git.Git Python.Python.3.13 astral-sh.uv OpenJS.NodeJS
   
   # 2. Navigate to existing repository on Drive E:
   cd E:\anti
   
   # 3. Restore Python dependencies via uv
   uv venv e:\anti\aios\.venv
   uv pip install -r e:\anti\aios\requirements.txt
   
   # 4. Run automated system health verification
   python e:\anti\aios\scripts\health_check.py
   ```

---

## 4. Restoration Verification Protocol (Non-Destructive Test)

A backup that has never been restored is merely a hypothesis. The following automated verification script runs weekly:
1. Creates a temporary sandbox directory: `E:\anti\aios\backups\restore_test_temp\`.
2. Extracts the latest backup archive into the sandbox.
3. Performs read operations, schema validations, and integrity checks against the restored SQLite database.
4. Generates a cryptographic SHA-256 hash match against the source.
5. Deletes the temporary sandbox and logs: `[VERIFIED] Backup integrity confirmed at YYYY-MM-DD`.
