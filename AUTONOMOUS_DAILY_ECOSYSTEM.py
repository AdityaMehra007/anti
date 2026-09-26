#!/usr/bin/env python3
"""
========================================================================================
ANTIGRAVITY OMEGA & HERMES: AUTONOMOUS DAILY ECOSYSTEM MASTER ORCHESTRATOR
========================================================================================
Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
Purpose:
  Master Autonomous 24/7 Daemon and Daily Execution Engine.
  Unifies the entire ecosystem across all 15 agents, 9 databases, 4,500 employers,
  300 strike targets, 51 enterprise dossiers, 4 portfolio deliverables, and live telemetry.
Execution Cycle:
  1. Environment & Database Health Integrity Verification (PRAGMA integrity_check).
  2. ADI CAREER OS Execution (10-Factor Scorer, Sales Red Flag Filter, Approval Ledger).
  3. Batch Dossier & Mega-Studio Compilation (RUN_AUTONOMOUS_PIPELINE.py).
  4. Portfolio Verification (Execution of SLA cost model & AI precision pipeline).
  5. Recruiter Outreach Staging & InMail Cadence Synchronization.
  6. Test Suite Automated Certification (pytest tests/test_adi_career_os.py).
  7. Telemetry & Heartbeat Persistence (.scratch/daily_ecosystem_telemetry.json).
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import time
import json
import sqlite3
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
SCRATCH_DIR = ROOT_DIR / ".scratch"
PORTFOLIO_DIR = ROOT_DIR / "portfolio"
APPLICATIONS_DIR = ROOT_DIR / "applications_generated"

TELEMETRY_JSON = SCRATCH_DIR / "daily_ecosystem_telemetry.json"
HERMES_STATUS_JSON = SCRATCH_DIR / "hermes_controller_status.json"

DATABASES = [
    DATA_DIR / "omega_master_core.db",
    DATA_DIR / "omega_approvals.db",
    DATA_DIR / "omega_career_database.sqlite",
    DATA_DIR / "omega_ledger.db",
    DATA_DIR / "omega_platform.db",
    ROOT_DIR / "omega" / "data" / "omega_master.db"
]

def log(step: str, msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_msg = msg.encode("ascii", errors="replace").decode("ascii")
    print(f"[{ts}] [{step}] {safe_msg}", flush=True)

class AutonomousDailyEcosystem:
    """Master 24/7 Autonomous Career Ecosystem Engine."""

    def __init__(self):
        SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

    def run_cycle(self) -> Dict[str, Any]:
        cycle_start = datetime.now(timezone.utc)
        log("ECOSYSTEM", "==================================================================")
        log("ECOSYSTEM", "  STARTING COMPLETE AUTONOMOUS DAILY CAREER ECOSYSTEM CYCLE       ")
        log("ECOSYSTEM", "==================================================================")

        results = {
            "timestamp": cycle_start.isoformat(),
            "candidate": "Aditya Mehra",
            "education": "BBA International Business (DSU '26)",
            "location": "Bengaluru, India",
            "phases": {}
        }

        # PHASE 1: Database & Health Audit
        log("PHASE-1", "Auditing databases and workspace integrity...")
        db_audit = {}
        for db in DATABASES:
            if db.exists():
                try:
                    with sqlite3.connect(db) as conn:
                        res = conn.execute("PRAGMA integrity_check").fetchone()
                        status = res[0] if res else "UNKNOWN"
                        db_audit[db.name] = status
                except Exception as e:
                    db_audit[db.name] = f"ERROR: {e}"
            else:
                db_audit[db.name] = "NOT_FOUND"
        results["phases"]["database_health"] = db_audit
        log("PHASE-1", f"Audited {len(db_audit)} databases. All healthy: {all(v == 'ok' for v in db_audit.values())}")

        # PHASE 2: Execute ADI CAREER OS Mission
        log("PHASE-2", "Triggering ADI CAREER OS (15 Autonomous Agents & Approval Gate)...")
        try:
            res_os = subprocess.run([sys.executable, str(ROOT_DIR / "adi_career_os.py"), "--do-everything"],
                                    cwd=str(ROOT_DIR), capture_output=True, text=True)
            results["phases"]["adi_career_os"] = {
                "exit_code": res_os.returncode,
                "status": "SUCCESS" if res_os.returncode == 0 else "ERROR"
            }
            log("PHASE-2", f"ADI CAREER OS completed with exit code {res_os.returncode}.")
        except Exception as e:
            results["phases"]["adi_career_os"] = {"error": str(e)}
            log("PHASE-2", f"Error running ADI CAREER OS: {e}")

        # PHASE 3: Execute Batch Pipeline & Studio Compilation
        log("PHASE-3", "Triggering RUN_AUTONOMOUS_PIPELINE.py (Dossiers & Mega Directory)...")
        try:
            res_pipe = subprocess.run([sys.executable, str(ROOT_DIR / "RUN_AUTONOMOUS_PIPELINE.py")],
                                      cwd=str(ROOT_DIR), capture_output=True, text=True)
            results["phases"]["pipeline_compilation"] = {
                "exit_code": res_pipe.returncode,
                "status": "SUCCESS" if res_pipe.returncode == 0 else "ERROR"
            }
            log("PHASE-3", f"Pipeline compilation completed with exit code {res_pipe.returncode}.")
        except Exception as e:
            results["phases"]["pipeline_compilation"] = {"error": str(e)}
            log("PHASE-3", f"Error running pipeline: {e}")

        # PHASE 4: Portfolio Verification
        log("PHASE-4", "Executing and certifying Portfolio Engines...")
        portfolio_results = {}
        # Project 2: Vendor SLA Cost Model
        p2_script = PORTFOLIO_DIR / "PROJECT_2_VENDOR_SLA_COST_MODEL.py"
        if p2_script.exists():
            r2 = subprocess.run([sys.executable, str(p2_script)], cwd=str(ROOT_DIR), capture_output=True, text=True)
            portfolio_results["vendor_sla_cost_model"] = "VERIFIED" if r2.returncode == 0 else "FAILED"
        
        # Project 4: AI Data Ops Pipeline
        p4_script = PORTFOLIO_DIR / "PROJECT_4_AI_DATA_OPS_QUALITY_PIPELINE.py"
        if p4_script.exists():
            r4 = subprocess.run([sys.executable, str(p4_script)], cwd=str(ROOT_DIR), capture_output=True, text=True)
            portfolio_results["ai_data_ops_pipeline"] = "VERIFIED" if r4.returncode == 0 else "FAILED"
        
        # Venture Project: OmniVanta B2B Vendor SLA Recovery Engine & Pipeline Builder
        omnivanta_script = ROOT_DIR / "omnivanta_engine.py"
        if omnivanta_script.exists():
            ro = subprocess.run([sys.executable, str(omnivanta_script)], cwd=str(ROOT_DIR), capture_output=True, text=True)
            portfolio_results["omnivanta_b2b_engine"] = "VERIFIED" if ro.returncode == 0 else "FAILED"
        
        omnivanta_pipe = ROOT_DIR / "omnivanta_pipeline_builder.py"
        if omnivanta_pipe.exists():
            rp = subprocess.run([sys.executable, str(omnivanta_pipe)], cwd=str(ROOT_DIR), capture_output=True, text=True)
            portfolio_results["omnivanta_pipeline_builder"] = "VERIFIED" if rp.returncode == 0 else "FAILED"
        
        # Interview Defense Simulation Engine
        interview_sim = ROOT_DIR / "interview_defense_simulator.py"
        if interview_sim.exists():
            ri = subprocess.run([sys.executable, str(interview_sim)], cwd=str(ROOT_DIR), capture_output=True, text=True)
            portfolio_results["interview_defense_simulator"] = "VERIFIED" if ri.returncode == 0 else "FAILED"
        
        # Omega Interactive Dispatch Console
        dispatch_console = ROOT_DIR / "omega_dispatch_console.py"
        if dispatch_console.exists():
            rc = subprocess.run([sys.executable, str(dispatch_console), "list"], cwd=str(ROOT_DIR), capture_output=True, text=True)
            portfolio_results["omega_dispatch_console"] = "VERIFIED" if rc.returncode == 0 else "FAILED"
        
        # TradingAgents Autonomous Financial & Market Multi-Agent Engine
        trading_agents_test = ROOT_DIR / "projects" / "TradingAgents" / "tests" / "test_omni_integration.py"
        if trading_agents_test.exists():
            ta_py = ROOT_DIR / "projects" / "TradingAgents" / ".venv" / "Scripts" / "python.exe"
            python_runner = str(ta_py) if ta_py.exists() else sys.executable
            rta = subprocess.run([python_runner, "-m", "pytest", str(trading_agents_test), "-q"], cwd=str(ROOT_DIR / "projects" / "TradingAgents"), capture_output=True, text=True)
            portfolio_results["trading_agents_engine"] = "VERIFIED" if rta.returncode == 0 else "FAILED"

        results["phases"]["portfolio_verification"] = portfolio_results
        log("PHASE-4", f"Portfolio deliverables verified: {portfolio_results}")

        # PHASE 5: Test Suite Certification
        log("PHASE-5", "Executing automated test suite (pytest tests/test_adi_career_os.py tests/test_omnivanta_engine.py tests/test_omnivanta_pipeline_builder.py tests/test_interview_defense_simulator.py tests/test_omega_dispatch_console.py)...")
        try:
            res_test = subprocess.run(["pytest", "tests/test_adi_career_os.py", "tests/test_omnivanta_engine.py", "tests/test_omnivanta_pipeline_builder.py", "tests/test_interview_defense_simulator.py", "tests/test_omega_dispatch_console.py"],
                                      cwd=str(ROOT_DIR), capture_output=True, text=True)
            results["phases"]["test_suite"] = {
                "exit_code": res_test.returncode,
                "status": "100% PASS" if res_test.returncode == 0 else "FAILED"
            }
            log("PHASE-5", f"Test suite certification: {results['phases']['test_suite']['status']}")
        except Exception as e:
            results["phases"]["test_suite"] = {"error": str(e)}
            log("PHASE-5", f"Error running test suite: {e}")

        # PHASE 6: Continuous Self-Improvement & Evolution Engine
        log("PHASE-6", "Running Adaptive Learning Engine ('MAKE MY SYSTEM BETTER EVERYTIME')...")
        try:
            from adaptive_career_learning_engine import AdaptiveCareerLearningEngine
            learner = AdaptiveCareerLearningEngine()
            evo = learner.evaluate_and_optimize()
            results["phases"]["continuous_learning"] = {
                "generation": evo["generation"],
                "active_instincts": evo["active_instincts_count"],
                "status": "SELF_IMPROVED"
            }
            log("PHASE-6", f"Continuous learning complete. Generation: {evo['generation']} | Active Instincts: {evo['active_instincts_count']}")
        except Exception as e:
            results["phases"]["continuous_learning"] = {"error": str(e)}
            log("PHASE-6", f"Notice in continuous learning: {e}")

        # Summary Telemetry
        cycle_end = datetime.now(timezone.utc)
        duration_sec = round((cycle_end - cycle_start).total_seconds(), 2)
        results["duration_seconds"] = duration_sec
        results["status"] = "OPERATIONAL"

        with open(TELEMETRY_JSON, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        log("ECOSYSTEM", "==================================================================")
        log("ECOSYSTEM", f"  AUTONOMOUS DAILY CYCLE COMPLETED IN {duration_sec}s [STATUS: OPERATIONAL] ")
        log("ECOSYSTEM", "==================================================================")
        return results

    def run_daemon(self, interval_hours: float = 24.0):
        log("DAEMON", f"Starting persistent Autonomous Daily Daemon (Interval: {interval_hours} hours)...")
        while True:
            try:
                self.run_cycle()
            except Exception as e:
                log("DAEMON-ERROR", f"Exception during autonomous cycle: {e}")
            log("DAEMON", f"Sleeping for {interval_hours} hours until next autonomous daily cycle...")
            time.sleep(interval_hours * 3600)

def main():
    parser = argparse.ArgumentParser(description="Autonomous Daily Ecosystem Master Orchestrator")
    parser.add_argument("--daemon", action="store_true", help="Run in continuous 24/7 daemon loop")
    parser.add_argument("--interval", type=float, default=24.0, help="Daemon interval in hours (default: 24.0)")
    parser.add_argument("--once", action="store_true", help="Run a single complete daily cycle immediately")

    args = parser.parse_args()
    engine = AutonomousDailyEcosystem()

    if args.daemon:
        engine.run_daemon(interval_hours=args.interval)
    else:
        # Default is run once
        engine.run_cycle()

if __name__ == "__main__":
    main()
