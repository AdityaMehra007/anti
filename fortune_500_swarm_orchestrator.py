"""
FORTUNE 500 SWARM ORCHESTRATOR & BATCH EXECUTION ENGINE
======================================================
Executes parallel multi-threaded swarm cycles across all 500 Fortune 500
enterprise codebases, collecting real-time execution telemetry and ROI ledgers.

Governed by OMEGA Constitution & ADI OMNI CODEX.
"""

import os
import sys
import json
import time
import importlib.util
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_DIR = os.path.join(BASE_DIR, "fortune_500_projects")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DATA_DIR = os.path.join(BASE_DIR, "data")
MASTER_JSON_PATH = os.path.join(DATA_DIR, "fortune_500_projects_master.json")
BATCH_REPORT_JSON = os.path.join(REPORTS_DIR, "fortune_500_batch_execution_report.json")
BATCH_REPORT_MD = os.path.join(REPORTS_DIR, "fortune_500_batch_execution_report.md")

os.makedirs(REPORTS_DIR, exist_ok=True)


def load_project_records() -> List[Dict[str, Any]]:
    if not os.path.exists(MASTER_JSON_PATH):
        raise FileNotFoundError(f"Missing master projects dataset: {MASTER_JSON_PATH}")
    with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["projects"]


def execute_single_project(project: Dict[str, Any]) -> Dict[str, Any]:
    """Dynamically loads and executes a single enterprise project's engine.py."""
    rank_str = f"{project['rank']:03d}"
    ticker = project['ticker']
    sector_dir = project['sector'].split('&')[0].strip().replace(' ', '_').replace('/', '_')
    engine_path = os.path.join(PROJECTS_DIR, sector_dir, f"rank_{rank_str}_{ticker}", "engine.py")

    t0 = time.perf_counter_ns()
    
    if not os.path.exists(engine_path):
        return {
            "rank": project["rank"],
            "company": project["company"],
            "ticker": ticker,
            "status": "ENGINE_FILE_MISSING",
            "latency_us": 0.0,
            "success": False
        }

    try:
        # Load module dynamically
        module_name = f"fortune500_rank_{rank_str}_{ticker.replace('.', '_')}"
        spec = importlib.util.spec_from_file_location(module_name, engine_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load spec for {engine_path}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        # Locate engine class
        class_name = f"{ticker.replace('.', '').replace('-', '')}ExecutiveEngine"
        engine_cls = getattr(mod, class_name, None)
        if engine_cls is None:
            raise AttributeError(f"Engine class {class_name} not found in {engine_path}")

        engine_inst = engine_cls()
        telemetry = engine_inst.execute_sovereign_cycle({"event": "SWARM_BATCH_PULSE", "timestamp": time.time()})
        t1 = time.perf_counter_ns()
        latency_us = (t1 - t0) / 1000.0

        return {
            "rank": project["rank"],
            "company": project["company"],
            "ticker": ticker,
            "sector": project["sector"],
            "project_codename": project["project_codename"],
            "status": telemetry.get("status", "EXECUTED"),
            "epoch": telemetry.get("epoch", 1),
            "modules_verified": telemetry.get("modules_verified", 4),
            "projected_roi_billion_usd": telemetry.get("projected_roi_billion_usd", 0.0),
            "latency_us": round(latency_us, 2),
            "success": True
        }
    except Exception as e:
        t1 = time.perf_counter_ns()
        return {
            "rank": project["rank"],
            "company": project["company"],
            "ticker": ticker,
            "status": "EXECUTION_ERROR",
            "error": str(e),
            "latency_us": round((t1 - t0) / 1000.0, 2),
            "success": False
        }


def run_swarm_batch(max_workers: int = 16, limit: int = None) -> Dict[str, Any]:
    """Executes all projects in parallel through high-concurrency worker threads."""
    projects = load_project_records()
    if limit is not None:
        projects = projects[:limit]

    total_count = len(projects)
    print(f"[*] Launching Swarm Orchestrator: {total_count} projects across {max_workers} parallel workers...")
    
    start_time = time.perf_counter()
    results = []
    success_count = 0
    total_roi_b = 0.0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {executor.submit(execute_single_project, p): p for p in projects}
        for future in as_completed(future_map):
            res = future.result()
            results.append(res)
            if res.get("success"):
                success_count += 1
                total_roi_b += res.get("projected_roi_billion_usd", 0.0)

    # Sort results by rank
    results.sort(key=lambda x: x["rank"])
    elapsed_s = time.perf_counter() - start_time
    avg_latency_us = sum(r["latency_us"] for r in results) / total_count if total_count > 0 else 0.0
    throughput_qps = total_count / elapsed_s if elapsed_s > 0 else 0.0

    report = {
        "metadata": {
            "orchestrator": "Fortune 500 Sovereign Swarm Dispatcher",
            "version": "1.0.0-OMEGA",
            "timestamp": time.time(),
            "workers_allocated": max_workers,
            "total_projects_dispatched": total_count,
            "successful_executions": success_count,
            "execution_rate_pct": round((success_count / total_count) * 100, 2),
            "total_batch_duration_seconds": round(elapsed_s, 3),
            "batch_throughput_projects_per_sec": round(throughput_qps, 2),
            "average_engine_latency_us": round(avg_latency_us, 2),
            "total_economic_value_unlocked_billion_usd": round(total_roi_b, 2),
            "total_economic_value_unlocked_trillion_usd": round(total_roi_b / 1000, 2)
        },
        "results_sample": results[:20],
        "all_results": results
    }

    # Save JSON Report
    with open(BATCH_REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Save Markdown Summary
    with open(BATCH_REPORT_MD, "w", encoding="utf-8") as f:
        f.write(f"# FORTUNE 500 SWARM BATCH EXECUTION REPORT\n\n")
        f.write(f"- **Total Projects Dispatched**: {total_count}\n")
        f.write(f"- **Successful Executions**: {success_count} ({round((success_count/total_count)*100, 1)}%)\n")
        f.write(f"- **Total Execution Time**: {round(elapsed_s, 3)} seconds\n")
        f.write(f"- **Throughput**: {round(throughput_qps, 1)} engines/second\n")
        f.write(f"- **Average Engine Latency**: {round(avg_latency_us, 2)} &mu;s\n")
        f.write(f"- **Total Economic Value Unlocked**: **${round(total_roi_b / 1000, 2)} Trillion USD**\n\n")
        f.write(f"## Top 20 Flagship Executions\n\n")
        f.write(f"| Rank | Company | Ticker | Project Codename | Modules | Latency (&mu;s) | ROI ($B) | Status |\n")
        f.write(f"| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for r in results[:20]:
            f.write(f"| #{r['rank']} | {r['company']} | `{r['ticker']}` | {r['project_codename']} | {r['modules_verified']} | {r['latency_us']} &mu;s | +${r['projected_roi_billion_usd']}B | **{r['status']}** |\n")

    print(f"[+] Swarm Execution Completed in {round(elapsed_s, 3)}s.")
    print(f"    - Success: {success_count}/{total_count} ({round((success_count/total_count)*100, 1)}%)")
    print(f"    - Throughput: {round(throughput_qps, 1)} engines/sec")
    print(f"    - Average Latency: {round(avg_latency_us, 2)} us")
    print(f"    - Reports written to: {BATCH_REPORT_JSON} & {BATCH_REPORT_MD}")

    return report


if __name__ == "__main__":
    run_swarm_batch(max_workers=16)
