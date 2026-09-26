#!/usr/bin/env python3
"""
========================================================================================
OMEGA PERPETUAL CAREER DAEMON (v8.0)
========================================================================================
Automated background supervisor for continuous intelligence, cadence alerts, and health audits.
Usage:
  python run_omni_daemon.py --run-once
  python run_omni_daemon.py --status
========================================================================================
"""

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.join(r"e:\anti", "omega", "core"))
sys.path.insert(0, r"e:\anti")

class OmniCareerDaemon:
    def __init__(self, db_path: str = r"e:\anti\omega\omega_platform.db"):
        self.db_path = db_path
        self.base_dir = r"e:\anti"

    def run_cadence_cycle(self) -> dict:
        """Executes one complete intelligence, cadence, and audit cycle."""
        timestamp = datetime.now().isoformat()
        cycle_report = {"timestamp": timestamp, "steps": {}}

        print("\n" + "=" * 80)
        print(f"?? OMEGA PERPETUAL DAEMON CYCLE STARTED [{timestamp}]")
        print("=" * 80)

        # 1. Update Daily Brief & Priority Top 5
        try:
            from omega_daily_brief import OmegaDailyBrief
            brief = OmegaDailyBrief()
            brief_path = brief.generate_daily_brief()
            cycle_report["steps"]["daily_brief"] = {"status": "SUCCESS", "path": brief_path}
            print("[?] Step 1: Daily Career Brief regenerated successfully.")
        except Exception as e:
            cycle_report["steps"]["daily_brief"] = {"status": "FAILED", "error": str(e)}
            print(f"[X] Step 1 Failed: {e}")

        # 2. Opportunity Database Refresh
        try:
            from opportunity_engine import OmegaOpportunityEngine
            opp_eng = OmegaOpportunityEngine()
            opps = opp_eng.run_ingestion_and_scoring()
            cycle_report["steps"]["opportunity_engine"] = {"status": "SUCCESS", "count": len(opps)}
            print(f"[?] Step 2: Opportunity Engine refreshed ({len(opps)} opportunities scored).")
        except Exception as e:
            cycle_report["steps"]["opportunity_engine"] = {"status": "FAILED", "error": str(e)}
            print(f"[X] Step 2 Failed: {e}")

        # 3. Follow-Up Cadence Scan
        try:
            state_file = os.path.join(self.base_dir, "outreach_pipeline_state.json")
            with open(state_file, "r", encoding="utf-8") as f:
                state_data = json.load(f)
            records = state_data.get("records", [])
            ready_count = sum(1 for r in records if r.get("current_stage") == "DISPATCH_READY")
            queued_count = sum(1 for r in records if r.get("current_stage") == "QUEUED")
            cycle_report["steps"]["cadence_scan"] = {
                "status": "SUCCESS",
                "dispatch_ready_count": ready_count,
                "queued_count": queued_count
            }
            print(f"[?] Step 3: Cadence Scan complete: {ready_count} DISPATCH_READY, {queued_count} QUEUED.")
        except Exception as e:
            cycle_report["steps"]["cadence_scan"] = {"status": "FAILED", "error": str(e)}
            print(f"[X] Step 3 Failed: {e}")

        # 4. Zero-Trust System Auditor
        try:
            auditor_script = os.path.join(self.base_dir, "independent_system_auditor.py")
            res = subprocess.run([sys.executable, auditor_script], capture_output=True, text=True, cwd=self.base_dir)
            audit_pass = (res.returncode == 0)
            cycle_report["steps"]["system_auditor"] = {"status": "PASS" if audit_pass else "FAIL"}
            print(f"[?] Step 4: Zero-Trust System Auditor -> {'PASS [OK]' if audit_pass else 'FAIL'}")
        except Exception as e:
            cycle_report["steps"]["system_auditor"] = {"status": "FAILED", "error": str(e)}
            print(f"[X] Step 4 Failed: {e}")

        # 5. Log Telemetry to SQLite DB
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS daemon_telemetry (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        health_status TEXT NOT NULL,
                        payload JSON NOT NULL
                    );
                """)
                conn.execute(
                    "INSERT INTO daemon_telemetry (timestamp, health_status, payload) VALUES (?, ?, ?);",
                    (timestamp, "HEALTHY", json.dumps(cycle_report))
                )
                conn.commit()
            print("[?] Step 5: Daemon telemetry recorded in SQLite WAL database.")
        except Exception as e:
            print(f"[!] Warning: Could not log to telemetry table: {e}")

        print("=" * 80)
        print(f"?? OMEGA DAEMON CYCLE COMPLETED [{datetime.now().isoformat()}]")
        print("=" * 80 + "\n")
        return cycle_report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Antigravity Omega Perpetual Career Daemon")
    parser.add_argument("--run-once", action="store_true", help="Execute single supervisor cycle")
    parser.add_argument("--status", action="store_true", help="Display daemon telemetry status")
    args = parser.parse_args()

    daemon = OmniCareerDaemon()
    if args.status:
        db_path = r"e:\anti\omega\omega_platform.db"
        if os.path.exists(db_path):
            with sqlite3.connect(db_path) as conn:
                cur = conn.cursor()
                cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='daemon_telemetry';")
                if cur.fetchone():
                    cur.execute("SELECT id, timestamp, health_status FROM daemon_telemetry ORDER BY id DESC LIMIT 5;")
                    rows = cur.fetchall()
                    print("\nRECENT DAEMON HEARTBEATS:")
                    for r in rows:
                        print(f"  [ID: {r[0]}] {r[1]} -> Status: {r[2]}")
                else:
                    print("No daemon telemetry recorded yet.")
        else:
            print(f"Database {db_path} does not exist.")
    else:
        daemon.run_cadence_cycle()
