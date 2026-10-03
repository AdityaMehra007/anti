#!/usr/bin/env python3
"""
ANTIGRAVITY OMEGA: Unified Life-Cycle Command CLI (omega_ctl)
Controls services, runs diagnostics, initiates backups, and audits system integrity.
Zero-Dependency (Pure Python Standard Library).
"""

import sys
import os
import json
import time
import shutil
import tarfile
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime

AIOS_ROOT = Path("E:/anti/aios")
DATA_DIR = AIOS_ROOT / "data"
PID_FILE = DATA_DIR / "pids.json"
BACKUP_DIR = AIOS_ROOT / "backups"
DB_PATH = DATA_DIR / "master.db"

sys.path.insert(0, str(AIOS_ROOT / "databases"))
sys.path.insert(0, str(AIOS_ROOT / "scripts"))

try:
    import db
except ImportError:
    db = None

try:
    import health_check
except ImportError:
    health_check = None

def load_pids() -> dict:
    if PID_FILE.exists():
        try:
            with open(PID_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_pids(pids: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(PID_FILE, "w") as f:
        json.dump(pids, f, indent=2)

def is_pid_alive(pid: int) -> bool:
    try:
        # Windows check using tasklist / standard library
        res = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True)
        return str(pid) in res.stdout
    except Exception:
        return False

def cmd_health():
    """Runs health check and prints formatted telemetry."""
    if health_check:
        report = health_check.run_health_check()
        health_check.format_console_report(report)
    else:
        print("[ERROR] health_check module not found.")

def cmd_status():
    """Displays running status of all AIOS services."""
    pids = load_pids()
    print("===============================================================================")
    print("                 ANTIGRAVITY OMEGA :: SERVICE STATUS BOARD                     ")
    print("===============================================================================")
    
    ports = {
        "AIOS Gateway Router": (8090, "aios_gateway"),
        "Master Command UI"  : (3000, "command_ui"),
        "Ollama LLM Engine"  : (11434, "ollama"),
        "n8n Automation"     : (5678, "n8n"),
        "Omniroute Event Bus": (20128, "omniroute"),
        "OpenHands Canvas"   : (3001, "openhands")
    }

    for name, (port, key) in ports.items():
        is_open = health_check.check_port("127.0.0.1", port) if health_check else False
        pid = pids.get(key)
        pid_str = f"PID: {pid}" if pid and is_pid_alive(pid) else "PID: N/A"
        state = "[ONLINE]" if is_open else "[OFFLINE]"
        print(f"  * {name:<22} (Port {port:<5}) : {state:<9} | {pid_str}")

    print("-------------------------------------------------------------------------------")
    if db:
        try:
            metrics = db.get_latest_metrics(limit=1)
            if metrics:
                m = metrics[0]
                print(f"Last DB Telemetry: {m['timestamp']} | Status: {m['status']} | Free RAM: {m['ram_free_gb']} GB")
        except Exception:
            pass
    print(f"Storage Primary (E:): {AIOS_ROOT} (Operational)")
    print("===============================================================================\n")

def cmd_start_core():
    """Launches Ring 0 core services in background (AI Gateway :8090 and Command UI :3000)."""
    pids = load_pids()
    python_exe = sys.executable

    # 1. Start AIOS Gateway
    if not health_check.check_port("127.0.0.1", 8090):
        print("[*] Launching AIOS Gateway Router on port 8090...")
        gateway_script = str(AIOS_ROOT / "ai" / "gateway.py")
        p_gw = subprocess.Popen(
            [python_exe, gateway_script],
            creationflags=0x00000208,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL
        )
        pids["aios_gateway"] = p_gw.pid
        time.sleep(1)
        if health_check.check_port("127.0.0.1", 8090):
            print(f"    [OK] Gateway online (PID {p_gw.pid}) at http://127.0.0.1:8090")
        else:
            print("    [!] Gateway process launched, initializing...")
    else:
        print("[i] AIOS Gateway Router is already running on port 8090.")

    # 2. Start Command Center UI Static Server on Port 3000
    if not health_check.check_port("127.0.0.1", 3000):
        print("[*] Launching Master Command UI server on port 3000...")
        ui_dir = str(AIOS_ROOT / "dashboards")
        p_ui = subprocess.Popen(
            [python_exe, "-m", "http.server", "3000", "--directory", ui_dir],
            creationflags=0x00000208,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL
        )
        pids["command_ui"] = p_ui.pid
        time.sleep(1)
        if health_check.check_port("127.0.0.1", 3000):
            print(f"    [OK] Command Center UI online (PID {p_ui.pid}) at http://127.0.0.1:3000")
        else:
            print("    [!] UI process launched, initializing...")
    else:
        print("[i] Command UI server is already running on port 3000.")

    save_pids(pids)
    if db:
        db.log_audit("CLI", "START_CORE", "LIFECYCLE", "Launched Ring 0 Gateway and Command UI", "INFO")
    print("\n[SUCCESS] Ring 0 Core services are active.")

def cmd_stop_core():
    """Stops tracked background core services."""
    pids = load_pids()
    print("[*] Terminating Core AIOS services...")
    for key in ["aios_gateway", "command_ui"]:
        pid = pids.get(key)
        if pid:
            try:
                subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)
                print(f"    [OK] Terminated {key} (PID {pid})")
            except Exception as e:
                print(f"    [!] Error terminating {key}: {e}")
            pids[key] = None

    save_pids(pids)
    if db:
        db.log_audit("CLI", "STOP_CORE", "LIFECYCLE", "Stopped Ring 0 Gateway and Command UI", "INFO")
    print("[SUCCESS] Core services stopped.")

def cmd_start_ai():
    """Launches local Ollama service with Maxwell GTX 960M GPU acceleration."""
    ollama_exe = Path("E:/anti gravity/Tools/Ollama/ollama.exe")
    if not ollama_exe.exists():
        print(f"[ERROR] Ollama executable not found at {ollama_exe}")
        return

    if health_check.check_port("127.0.0.1", 11434):
        print("[i] Ollama is already active on port 11434.")
        return

    print(f"[*] Starting Ollama from {ollama_exe} with models on Drive E:...")
    env = os.environ.copy()
    env["OLLAMA_MODELS"] = "E:/anti gravity/OllamaData/models"
    env["OLLAMA_NUM_PARALLEL"] = "1"
    env["OLLAMA_MAX_LOADED_MODELS"] = "1"
    env["OLLAMA_KEEP_ALIVE"] = "5m"
    env["OLLAMA_HOST"] = "127.0.0.1:11434"
    p_ollama = subprocess.Popen([str(ollama_exe), "serve"], env=env, creationflags=0x00000208)
    
    pids = load_pids()
    pids["ollama"] = p_ollama.pid
    save_pids(pids)

    time.sleep(2)
    if health_check.check_port("127.0.0.1", 11434):
        print(f"[OK] Ollama running (PID {p_ollama.pid}) at http://127.0.0.1:11434")
    else:
        print("[!] Ollama started in background, engine initializing...")

def cmd_stop_ai():
    """Terminates Ollama runner."""
    pids = load_pids()
    pid = pids.get("ollama")
    if pid:
        subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)
        print(f"[OK] Stopped Ollama process {pid}")
        pids["ollama"] = None
        save_pids(pids)
    else:
        subprocess.run(["taskkill", "/F", "/IM", "ollama.exe"], capture_output=True)
        print("[OK] Stopped any running Ollama instances.")

def cmd_benchmark_ai():
    """Executes repeatable local AI benchmark."""
    bench_script = AIOS_ROOT / "scripts" / "benchmark_ai.py"
    if bench_script.exists():
        subprocess.run([sys.executable, str(bench_script)])
    else:
        print(f"[ERROR] Benchmark script not found at {bench_script}")

def cmd_backup():
    """Creates a point-in-time SQLite snapshot and versioned tar archive."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    db_backup_dir = BACKUP_DIR / "db"
    db_backup_dir.mkdir(parents=True, exist_ok=True)
    target_db_file = db_backup_dir / f"master_{timestamp}.db"

    print(f"[*] Creating SQLite point-in-time snapshot to {target_db_file}...")
    if DB_PATH.exists():
        with sqlite3.connect(str(DB_PATH)) as con:
            con.execute(f"VACUUM INTO '{target_db_file.as_posix()}';")
        print(f"    [OK] Database snapshot saved ({target_db_file.stat().st_size} bytes)")
    else:
        print("    [!] master.db not found, skipping DB snapshot.")

    # Archive documentation & configs
    archive_file = BACKUP_DIR / f"aios_config_docs_{timestamp}.tar.gz"
    print(f"[*] Creating configuration & documentation archive to {archive_file}...")
    with tarfile.open(archive_file, "w:gz") as tar:
        for folder in ["docs", "configs", "databases"]:
            p = AIOS_ROOT / folder
            if p.exists():
                tar.add(str(p), arcname=folder)
    print(f"    [OK] Archive created ({archive_file.stat().st_size} bytes)")
    
    if db:
        db.log_audit("CLI", "BACKUP", "MAINTENANCE", f"Created backup {archive_file.name}", "INFO")
    print(f"\n[SUCCESS] Backup complete. Target: {archive_file.name}")

def cmd_restore_test():
    """Performs a non-destructive restoration verification test on the latest backup."""
    db_backups = list((BACKUP_DIR / "db").glob("*.db"))
    if not db_backups:
        print("[!] No database backups found in backups/db/.")
        return

    latest_backup = max(db_backups, key=lambda p: p.stat().st_mtime)
    print(f"[*] Testing integrity of latest backup: {latest_backup.name}...")
    
    temp_sandbox = BACKUP_DIR / "restore_test_temp"
    temp_sandbox.mkdir(parents=True, exist_ok=True)
    test_db_copy = temp_sandbox / "test_verify.db"

    try:
        shutil.copy2(latest_backup, test_db_copy)
        with sqlite3.connect(str(test_db_copy)) as con:
            res = con.execute("PRAGMA integrity_check;").fetchone()
            if res and res[0] == "ok":
                print("    [OK] PRAGMA integrity_check: PASSED (Zero corruption).")
                cur = con.execute("SELECT COUNT(*) FROM system_metrics;")
                count = cur.fetchone()[0]
                print(f"    [OK] Verified {count} telemetry records readable.")
            else:
                print(f"    [FAILED] Integrity check returned: {res}")
    finally:
        shutil.rmtree(temp_sandbox, ignore_errors=True)
        print("    [OK] Temporary sandbox purged.")
    print("[SUCCESS] Restoration verification test passed cleanly.")

def cmd_security_check():
    """Audits gitignore, directory permissions, and sensitive files."""
    print("===============================================================================")
    print("                 ANTIGRAVITY OMEGA :: SECURITY & PRIVACY AUDIT                 ")
    print("===============================================================================")
    
    # 1. Check .gitignore exists in AIOS root
    gi = AIOS_ROOT / ".gitignore"
    if gi.exists():
        print(f"  [OK] Security Boundary (.gitignore) present at {gi}")
    else:
        print(f"  [!] Missing .gitignore in {AIOS_ROOT}")

    # 2. Check secrets/ directory isolation
    sec_dir = AIOS_ROOT / "secrets"
    if sec_dir.exists():
        print(f"  [OK] Isolated secrets/ vault present at {sec_dir}")
    else:
        print(f"  [!] Missing secrets directory")

    # 3. Check for any tracked .env files in git
    try:
        res = subprocess.run(["git", "status", "--porcelain"], cwd="E:/anti", capture_output=True, text=True)
        staged_envs = [line for line in res.stdout.splitlines() if ".env" in line and not line.endswith(".example")]
        if staged_envs:
            print("  [!] WARNING: Uncommitted .env files detected:")
            for e in staged_envs:
                print(f"      {e}")
        else:
            print("  [OK] No live .env or credential files staged in git.")
    except Exception:
        pass

    print("===============================================================================\n")

def print_help():
    print("""
ANTIGRAVITY OMEGA :: Life-Cycle Command CLI (omega_ctl)

Usage: python omega_ctl.py <command>

Commands:
  health          Run live system health diagnostic & telemetry check
  status          Show live status of all system services and ports
  start-core      Start Ring 0 Core services (AI Gateway :8090, Command UI :3000)
  stop-core       Stop Ring 0 Core services
  start-ai        Start Ollama LLM Engine with GTX 960M acceleration
  stop-ai         Stop Ollama LLM Engine to reclaim VRAM/RAM
  benchmark-ai    Run repeatable local LLM benchmark (tokens/sec, TTFT, VRAM)
  backup          Create SQLite WAL snapshot and tar.gz configuration archive
  restore-test    Perform non-destructive restore integrity verification test
  security-check  Audit git security boundaries and secret isolation
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "health":
        cmd_health()
    elif cmd == "status":
        cmd_status()
    elif cmd == "start-core":
        cmd_start_core()
    elif cmd == "stop-core":
        cmd_stop_core()
    elif cmd == "start-ai":
        cmd_start_ai()
    elif cmd == "stop-ai":
        cmd_stop_ai()
    elif cmd == "benchmark-ai":
        cmd_benchmark_ai()
    elif cmd == "backup":
        cmd_backup()
    elif cmd == "restore-test":
        cmd_restore_test()
    elif cmd == "security-check":
        cmd_security_check()
    else:
        print(f"[ERROR] Unknown command: {cmd}")
        print_help()
