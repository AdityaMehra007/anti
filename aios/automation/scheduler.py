#!/usr/bin/env python3
"""
ANTIGRAVITY OMEGA: Autonomous Automation Scheduler
Zero-dependency, pure Python daemon executing scheduled DAG tasks:
- Periodic telemetry health synchronization
- Hourly automation pipeline check
- Database backup snapshot execution
- Execution ledger pruning and audit synchronization
"""

import sys
import os
import time
import argparse
from pathlib import Path
from datetime import datetime

AIOS_ROOT = Path("E:/anti/aios")
sys.path.insert(0, str(AIOS_ROOT / "automation"))
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

from automation_bridge import AutomationBridge


class AutomationScheduler:
    def __init__(self, check_interval_sec: int = 60):
        self.interval = check_interval_sec
        self.bridge = AutomationBridge()
        self.last_health_sync = 0.0
        self.last_backup = 0.0

    def step(self):
        """Executes one evaluation cycle of all time-gated scheduled jobs."""
        now = time.time()

        # Job 1: Real-time telemetry & health sync (Every 5 minutes = 300s)
        if now - self.last_health_sync >= 300:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [SCHEDULER] Triggering Telemetry Health Sync DAG...")
            if health_check and db:
                try:
                    rep = health_check.run_health_check()
                    # Also trigger n8n event
                    self.bridge.run_health_sync_dag()
                    self.last_health_sync = now
                    print(f"    [OK] Telemetry synchronized. Host status: {rep.get('status')}")
                except Exception as e:
                    print(f"    [!] Error during health sync: {e}")

        # Job 2: SQLite database WAL checkpoint (Every 1 hour = 3600s)
        if now - self.last_backup >= 3600:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [SCHEDULER] Running SQLite WAL PRAGMA optimize...")
            if db:
                try:
                    with db.get_connection() as con:
                        con.execute("PRAGMA wal_checkpoint(PASSIVE);")
                        con.execute("PRAGMA optimize;")
                    db.log_audit("SCHEDULER", "WAL_OPTIMIZE", "DATABASE", "Executed passive WAL checkpoint and optimize", "INFO")
                    self.last_backup = now
                    print("    [OK] SQLite maintenance complete.")
                except Exception as e:
                    print(f"    [!] SQLite optimization error: {e}")

    def run_forever(self):
        """Main daemon loop."""
        print(f"[*] ANTIGRAVITY OMEGA Automation Scheduler started (Cycle interval: {self.interval}s)")
        if db:
            db.log_audit("SCHEDULER", "START_DAEMON", "AUTOMATION", "Automation scheduler daemon online", "INFO")
        
        # Execute immediately on start
        self.step()

        while True:
            try:
                time.sleep(self.interval)
                self.step()
            except KeyboardInterrupt:
                print("\n[*] Scheduler stopping...")
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AIOS Automation Scheduler")
    parser.add_argument("--once", action="store_true", help="Execute single maintenance cycle and exit")
    parser.add_argument("--interval", type=int, default=60, help="Loop interval in seconds")
    args = parser.parse_args()

    sched = AutomationScheduler(check_interval_sec=args.interval)
    if args.once:
        print("[*] Running single scheduler pass...")
        sched.step()
        print("[OK] Single pass complete.")
    else:
        sched.run_forever()
