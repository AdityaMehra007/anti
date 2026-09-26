"""
Nous Research Hermes Agent — Master Autonomous Controller & Supervisor
Maintains 24/7 background control, self-healing, web dashboard watchdog,
cron scheduler execution, and database maintenance in e:\\anti.
"""

import json
import os
import sqlite3
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(r"e:\anti")
HERMES_REPO = WORKSPACE / "external" / "hermes-agent"
VENV_PYTHON = HERMES_REPO / ".venv" / "Scripts" / "python.exe"
STATUS_FILE = WORKSPACE / ".scratch" / "hermes_controller_status.json"
HERMES_HOME = Path(os.environ.get("LOCALAPPDATA", r"C:\Users\amehr\AppData\Local")) / "hermes"
DB_PATH = HERMES_HOME / "state.db"

DASHBOARD_PORT = 9119
DASHBOARD_URL = f"http://127.0.0.1:{DASHBOARD_PORT}"

# Environment for subprocess calls
ENV = os.environ.copy()
ENV["PYTHONIOENCODING"] = "utf-8"
ENV["HERMES_HOME"] = str(HERMES_HOME)


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_msg = msg.encode("ascii", errors="replace").decode("ascii")
    print(f"[{ts}] [HERMES-CONTROLLER] {safe_msg}", flush=True)


def is_dashboard_alive() -> bool:
    """Check if the dashboard HTTP server answers on port 9119."""
    try:
        req = urllib.request.Request(DASHBOARD_URL, headers={"User-Agent": "HermesSupervisor/1.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False


def start_dashboard():
    """Launch the Web Dashboard detached in the background."""
    log(f"Spawning Hermes Web Dashboard on port {DASHBOARD_PORT}...")
    cmd = [
        str(VENV_PYTHON),
        "-m", "hermes_cli.main",
        "dashboard",
        "--skip-build",
        "--no-open",
        "--port", str(DASHBOARD_PORT)
    ]
    # DETACHED_PROCESS flag on Windows
    creationflags = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    try:
        subprocess.Popen(
            cmd,
            cwd=str(HERMES_REPO),
            env=ENV,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags
        )
        log("Dashboard spawn request submitted.")
    except Exception as exc:
        log(f"Failed to spawn dashboard: {exc}")


def tick_cron():
    """Trigger scheduled cron jobs once."""
    cmd = [str(VENV_PYTHON), "-m", "hermes_cli.main", "cron", "tick"]
    try:
        res = subprocess.run(
            cmd,
            cwd=str(HERMES_REPO),
            env=ENV,
            capture_output=True,
            text=True,
            timeout=30
        )
        if res.returncode == 0 and res.stdout.strip():
            log(f"Cron tick result: {res.stdout.strip()[:100]}")
    except Exception as exc:
        log(f"Cron tick check: {exc}")


def optimize_database():
    """Run SQLite WAL checkpoint and optimization on state.db."""
    if not DB_PATH.exists():
        return
    try:
        conn = sqlite3.connect(str(DB_PATH), timeout=5)
        cursor = conn.cursor()
        cursor.execute("PRAGMA wal_checkpoint(PASSIVE);")
        cursor.execute("PRAGMA optimize;")
        conn.commit()
        conn.close()
    except Exception as exc:
        log(f"Database optimization note: {exc}")


def run_autonomous_career_pipeline():
    """Trigger the autonomous career pipeline script."""
    cmd = [str(VENV_PYTHON), str(WORKSPACE / "RUN_AUTONOMOUS_PIPELINE.py")]
    try:
        res = subprocess.run(
            cmd,
            cwd=str(WORKSPACE),
            capture_output=True,
            text=True,
            timeout=120
        )
        if res.returncode == 0:
            log("Autonomous career pipeline executed successfully.")
        else:
            log(f"Career pipeline run note: {res.stderr[:100]}")
    except Exception as exc:
        log(f"Career pipeline execution error: {exc}")


def update_status(dashboard_ok: bool, cycles: int, start_time: float):
    """Write controller heartbeat to status JSON file."""
    uptime_sec = int(time.time() - start_time)
    payload = {
        "status": "OPERATIONAL",
        "last_heartbeat": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": uptime_sec,
        "cycles_completed": cycles,
        "dashboard_port": DASHBOARD_PORT,
        "dashboard_healthy": dashboard_ok,
        "active_workspace": str(WORKSPACE),
        "total_skills_mounted": 3679,
        "controller_pid": os.getpid()
    }
    try:
        STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = STATUS_FILE.with_name(STATUS_FILE.name + ".tmp")
        tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        tmp.replace(STATUS_FILE)
    except Exception:
        pass


def main():
    log("=================================================================")
    log("  HERMES AGENT AUTONOMOUS CONTROLLER & SUPERVISOR INITIALIZED")
    log("=================================================================")
    log(f"Controller PID: {os.getpid()}")
    log(f"Workspace     : {WORKSPACE}")
    log(f"Target Port   : {DASHBOARD_PORT}")

    start_time = time.time()
    cycles = 0
    last_cron_tick = 0
    last_db_opt = 0
    last_pipeline_run = time.time()  # Initialized; runs every 6 hours

    while True:
        try:
            now = time.time()
            cycles += 1

            # 1. Health check Web Dashboard
            dashboard_ok = is_dashboard_alive()
            if not dashboard_ok:
                log("Dashboard down or unresponsive. Initiating auto-recovery...")
                start_dashboard()
                time.sleep(4)
                dashboard_ok = is_dashboard_alive()
                if dashboard_ok:
                    log("[OK] Dashboard successfully restored on http://127.0.0.1:9119")
                else:
                    log("[WARN] Dashboard restart in progress...")

            # 2. Tick Cron scheduler every 60s
            if now - last_cron_tick >= 60:
                tick_cron()
                last_cron_tick = now

            # 3. Optimize database every 10 minutes
            if now - last_db_opt >= 600:
                optimize_database()
                last_db_opt = now

            # 4. Run autonomous career pipeline every 6 hours
            if now - last_pipeline_run >= 21600:
                run_autonomous_career_pipeline()
                last_pipeline_run = now

            # 5. Update status file
            update_status(dashboard_ok, cycles, start_time)

            # Sleep between check intervals (10 seconds)
            time.sleep(10)

        except KeyboardInterrupt:
            log("Autonomous controller stopped by user.")
            break
        except Exception as exc:
            log(f"Controller loop error: {exc}")
            time.sleep(10)


if __name__ == "__main__":
    main()
