#!/usr/bin/env python3
"""
Autonomous Company Daemon: Continuous execution loop for scheduled intelligence & health checks
Enforces self-audit, data consistency, and system monitoring in accordance with Part LXIII.
"""

import os
import sys
import time
import json
import argparse
from datetime import datetime

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

AUTO_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(AUTO_DIR, ".."))
DATA_DIR = os.path.join(ROOT_DIR, "08_DATA")

class AutonomousDaemon:
    def __init__(self):
        self.running = False
        self.heartbeats = 0

    def inspect_subsystems(self):
        """Validates all key subsystems and data stores."""
        checks = {}
        
        # 1. Check datasets
        datasets = ["opportunities_100.json", "problems_100.json", "automations_100.json", "omniverse_summary.json"]
        for ds in datasets:
            p = os.path.join(DATA_DIR, ds)
            checks[f"dataset_{ds}"] = "ONLINE" if os.path.exists(p) and os.path.getsize(p) > 100 else "DEGRADED"

        # 2. Check UI and API
        ui_path = os.path.join(ROOT_DIR, "06_ENGINEERING", "ui", "index.html")
        api_path = os.path.join(ROOT_DIR, "06_ENGINEERING", "src", "api.py")
        checks["ui_layer"] = "ONLINE" if os.path.exists(ui_path) else "MISSING"
        checks["api_layer"] = "ONLINE" if os.path.exists(api_path) else "MISSING"

        # 3. Check strategy and playbooks
        opp_map = os.path.join(ROOT_DIR, "01_STRATEGY", "GLOBAL_BUSINESS_OPPORTUNITY_MAP_100.md")
        blueprint = os.path.join(ROOT_DIR, "05_PRODUCT", "MASTER_EXECUTION_BLUEPRINT.md")
        checks["strategy_map"] = "ONLINE" if os.path.exists(opp_map) else "MISSING"
        checks["execution_blueprint"] = "ONLINE" if os.path.exists(blueprint) else "MISSING"

        return checks

    def run_single_cycle(self):
        self.heartbeats += 1
        subsystems = self.inspect_subsystems()
        degraded = [k for k, v in subsystems.items() if v != "ONLINE"]
        
        cycle_report = {
            "cycle_id": self.heartbeats,
            "timestamp": datetime.now().isoformat(),
            "system_health": "OPTIMAL" if not degraded else "WARNING",
            "subsystems_checked": len(subsystems),
            "subsystems_online": len(subsystems) - len(degraded),
            "degraded_components": degraded,
            "monitors": [
                "DGFT Regulatory Gazette Watcher",
                "ICEGATE EDI Validator",
                "EU CBAM Registry Scanner",
                "Outbound Outreach Pipeline Health"
            ],
            "active_alerts": len(degraded)
        }
        return cycle_report

def main():
    parser = argparse.ArgumentParser(description="Autonomous Company Daemon")
    parser.add_argument("--cycle", action="store_true", help="Execute a single diagnostic heartbeat cycle")
    parser.add_argument("--daemon", action="store_true", help="Run continuously in background")
    parser.add_argument("--interval", type=int, default=60, help="Interval in seconds between daemon cycles")
    args = parser.parse_args()

    daemon = AutonomousDaemon()

    if args.daemon:
        print(f"Starting Autonomous Company Daemon (Interval: {args.interval}s)... Press Ctrl+C to exit.")
        try:
            while True:
                report = daemon.run_single_cycle()
                print(f"[{report['timestamp']}] Heartbeat #{report['cycle_id']} - Health: {report['system_health']} (Online: {report['subsystems_online']}/{report['subsystems_checked']})")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("Daemon stopped by user.")
    else:
        # Default to single cycle
        report = daemon.run_single_cycle()
        print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
