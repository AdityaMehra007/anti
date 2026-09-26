"""
AQUA Autonomous System Daemon (ANTIGRAVITY Ω∞)
Operates continuous background monitoring, pipeline progression,
subsystem health audits, and decision calibration tracking.
"""

import os
import sys
import time
import json
import argparse
from typing import Dict, Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from core.aqua_core import AquaCore
from aqua.crm_tracker import PipelineCRM
from aqua.decision_journal import DecisionJournal

class AquaDaemon:
    def __init__(self, workspace_root: str = "e:/anti", state_file: str = None):
        self.workspace_root = workspace_root
        self.state_file = state_file or os.path.join(workspace_root, "aqua", "daemon_state.json")
        self.core = AquaCore(workspace_root=workspace_root)
        self.crm = PipelineCRM()
        self.journal = DecisionJournal(os.path.join(workspace_root, "aqua", "decision_journal.jsonl"))

    def run_cycle(self) -> Dict[str, Any]:
        """
        Executes a single autonomous health, pipeline, and progression cycle.
        """
        now = time.time()
        now_str = time.strftime("%Y-%m-%d %H:%M:%S IST", time.localtime(now))

        # 1. System Health
        health = self.core.run_system_health_audit()

        # 2. CRM Telemetry
        crm_metrics = self.crm.calculate_pipeline_metrics()

        # 3. Decision Calibration
        calib_stats = self.journal.calculate_calibration_stats()

        # 4. Trillion-Dollar Ladder
        ladder = self.core.evaluate_trillion_dollar_ladder(current_arr_usd=0.0)

        # 5. Stale Account Detection
        stale_accounts = []
        accounts = self.crm.list_accounts()
        for a in accounts:
            # If account in OUTREACH_READY has no follow-up for > 48 hours (simulated check)
            if a["stage"] == "OUTREACH_READY":
                stale_accounts.append({
                    "account_id": a["account_id"],
                    "company_name": a["company_name"],
                    "demurrage_usd": a["demurrage_exposure_usd"],
                    "action_required": "Dispatch personalized outreach email to target executive"
                })

        state = {
            "timestamp": now,
            "timestamp_str": now_str,
            "status": "OPERATIONAL",
            "health_status": health["overall_status"],
            "subsystems_online": health["checks"]["subsystems_registered_count"],
            "active_ladder_stage": ladder["active_stage"]["tier"],
            "ladder_target": ladder["next_target_stage"]["label"],
            "pipeline": {
                "accounts_count": crm_metrics["total_accounts"],
                "demurrage_usd": crm_metrics["total_demurrage_identified_usd"],
                "potential_mrr_inr": crm_metrics["potential_pipeline_mrr_inr"],
                "potential_arr_usd": crm_metrics["potential_pipeline_arr_usd"],
                "weighted_arr_usd": crm_metrics["weighted_arr_usd"]
            },
            "calibration": calib_stats,
            "pending_founder_actions_count": len(stale_accounts),
            "top_stale_accounts": stale_accounts[:5]
        }

        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

        return state

    def start_loop(self, interval_seconds: int = 60, max_cycles: int = 1):
        cycles = 0
        while max_cycles <= 0 or cycles < max_cycles:
            state = self.run_cycle()
            print(f"[{state['timestamp_str']}] Daemon cycle #{cycles+1} completed. Status: {state['status']} | Subsystems: {state['subsystems_online']}/22 | Pipeline: {state['pipeline']['accounts_count']} accounts")
            cycles += 1
            if max_cycles <= 0 or cycles < max_cycles:
                time.sleep(interval_seconds)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AQUA Autonomous System Daemon")
    parser.add_argument("--once", action="store_true", help="Run a single cycle and exit")
    parser.add_argument("--cycles", type=int, default=1, help="Number of cycles to execute (default: 1)")
    parser.add_argument("--interval", type=int, default=30, help="Interval between cycles in seconds")
    args = parser.parse_args()

    daemon = AquaDaemon()
    if args.once or args.cycles == 1:
        st = daemon.run_cycle()
        print(f"AQUA Daemon cycle executed successfully. Saved to {daemon.state_file}")
        print(json.dumps(st, indent=2))
    else:
        daemon.start_loop(interval_seconds=args.interval, max_cycles=args.cycles)
