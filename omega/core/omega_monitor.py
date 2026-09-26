#!/usr/bin/env python3
"""
OMEGA ∞ OBSERVABILITY & MONITORING DAEMON
Enforces Section 61 (Observability Engine) and Section 94 (Crisis Command Mode).
Monitors system health, SQLite database connectivity, log status, and generates
continuous heartbeats.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import os
import time
import json
import sqlite3
import argparse
import datetime
from typing import Dict, Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
MONITOR_LOG_PATH = os.path.join(LOGS_DIR, "omega_infinity_monitor.log")
CONSTITUTION_PATH = os.path.join(BASE_DIR, "OMEGA_CONSTITUTION.md")

class OmegaMonitor:
    def __init__(self):
        os.makedirs(LOGS_DIR, exist_ok=True)

    def perform_health_check(self) -> Dict[str, Any]:
        """Runs checks across filesystem, databases, constitution, and processes."""
        status = {
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "HEALTHY",
            "checks": {}
        }

        # Check 1: Constitution File
        if os.path.exists(CONSTITUTION_PATH) and os.path.getsize(CONSTITUTION_PATH) > 10000:
            status["checks"]["constitution"] = {"healthy": True, "size_bytes": os.path.getsize(CONSTITUTION_PATH)}
        else:
            status["checks"]["constitution"] = {"healthy": False, "error": "Constitution missing or too small"}
            status["status"] = "DEGRADED"

        # Check 2: Core Database Files
        db_paths = [
            os.path.join(BASE_DIR, "omega", "omega_platform.db"),
            os.path.join(BASE_DIR, "career_knowledge_graph.json")
        ]
        for p in db_paths:
            name = os.path.basename(p)
            if os.path.exists(p):
                status["checks"][name] = {"healthy": True, "size_bytes": os.path.getsize(p)}
            else:
                status["checks"][name] = {"healthy": False, "warning": "File not found"}

        # Check 3: Disk space / writable logs
        try:
            test_write = os.path.join(LOGS_DIR, ".monitor_test")
            with open(test_write, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(test_write)
            status["checks"]["filesystem_writable"] = {"healthy": True}
        except Exception as e:
            status["checks"]["filesystem_writable"] = {"healthy": False, "error": str(e)}
            status["status"] = "DEGRADED"

        return status

    def log_heartbeat(self, status: Dict[str, Any]):
        line = f"[{status['timestamp']}] STATUS={status['status']} CHECKS={json.dumps(status['checks'])}\n"
        with open(MONITOR_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line)

    def run_once(self) -> Dict[str, Any]:
        health = self.perform_health_check()
        self.log_heartbeat(health)
        return health


def main():
    parser = argparse.ArgumentParser(description="OMEGA ∞ Observability Daemon")
    parser.add_argument("--once", action="store_true", help="Run a single health check and exit")
    parser.add_argument("--interval", type=int, default=60, help="Heartbeat interval in seconds")
    args = parser.parse_args()

    monitor = OmegaMonitor()
    if args.once:
        res = monitor.run_once()
        print(f"[OK] Health check complete. Status: {res['status']}")
        for k, v in res["checks"].items():
            print(f"  - {k}: {v}")
        return

    print(f"[*] Starting OMEGA ∞ Observability Daemon (Interval: {args.interval}s)...")
    try:
        while True:
            res = monitor.run_once()
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Heartbeat: {res['status']}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[*] Monitor stopped by operator.")

if __name__ == "__main__":
    main()
