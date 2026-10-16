# SECURITY, DATA PROTECTION & DISASTER RECOVERY PROTOCOL

**Document ID:** `SEC-REC-OMNI-2026-10-16`  
**System:** Google Antigravity Workstation Command Center  
**Classification:** Operational Security & Resilience Guide  

---

## 1. Core Security Principles

1. **Zero Secret Exposure:**
   - Never hardcode API keys, personal passwords, or authentication bearer tokens into source code, documentation, or commits.
   - All external keys (Google AI Studio, OpenAI, GitHub, Supabase) must reside strictly in local `.env` files that are ignored by Git.
   - Scripts and logs must sanitize and mask credentials (`sk-...****`).

2. **Least Privilege Execution:**
   - Execute all build scripts, tests, and workers under standard user privileges.
   - Never execute elevated PowerShell commands (`Run as Administrator`) unless explicitly performing an operating system level driver installation.

3. **Untrusted Data Sanitization:**
   - External web scraping content (e.g. from job boards or company pages) must be parsed as plain untrusted data strings.
   - Never evaluate or execute scraped HTML/JavaScript strings via `eval()` or shell execution.

4. **Private Candidate Data Isolation:**
   - Keep candidate personal contact numbers, residential address, and unredacted identification documents out of public repositories.
   - Distribute only verified, professional career URLs and contacts.

---

## 2. Standard `.gitignore` Protection

Ensure the following rules are present in the project `.gitignore`:
```gitignore
# Environment & Secrets
.env
*.env
*.key
*.pem
credentials.json
secrets.yaml

# Local Databases & Logs
*.db
*.sqlite
*.sqlite3
*.log
system_event_log.jsonl

# Python Virtual Environments & Cache
__pycache__/
*.py[cod]
.venv/
venv/
env/
.pytest_cache/

# Node & Build Artifacts
node_modules/
dist/
.cache/
```

---

## 3. Disaster Recovery & Backup Protocol

### A. Local Snapshot Backup
A lightweight backup script (`automation/backup_vault.py`) creates compressed timestamped snapshots of `career_vault.db` and configuration markdown files in `E:\anti\AI-Command-Center\backups\`.

```bash
# Manual snapshot command
python automation/backup_vault.py
```

### B. SQLite Database Recovery Protocol
If `career_vault.db` ever experiences unexpected locking, file corruption, or accidental row deletion:
1. Stop any running dashboard or worker processes.
2. Check the most recent snapshot in `backups/`.
3. If no recent snapshot exists, execute SQLite salvage:
   ```bash
   sqlite3 career_vault.db ".recover" | sqlite3 career_vault_recovered.db
   ```
4. Re-run `python career_engine.py` to re-seed verified core requisitions.

### C. Process Freeze & Port Collision Triage
If a local web server (e.g. port 8050 or 3000) freezes or fails with `EADDRINUSE`:
```powershell
# Identify process holding port 8050
Get-NetTCPConnection -LocalPort 8050 | Select-Object OwningProcess

# Terminate orphaned process safely
Stop-Process -Id <PID> -Force
```

### D. System Drive (`C:\`) Emergency Cleanup
If `C:\` space drops below 10 GB:
1. Purge npm cache: `npm cache clean --force`
2. Purge pip cache: `pip cache purge`
3. Verify Hugging Face and Ollama model weights remain strictly on `E:\`.
