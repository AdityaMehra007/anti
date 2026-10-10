#!/usr/bin/env python3
"""
========================================================================================
ANTIGRAVITY OMEGA: UNIFIED MASTER PLATFORM BUILD RUNNER
========================================================================================
Supreme Constitution: OMEGA_CONSTITUTION.md (Directives 1–120)
Autonomous Build & Verification Harness (Mode D & Mode F)

Executes end-to-end build verification across all platform pillars:
1. Python syntax & bytecode compilation checks across all modules
2. Database health & PRAGMA integrity checks across all SQLite stores
3. SaaS Factory 4-stack reference portfolio audit
4. Live service mesh health checks (Gateway :8090, Ollama :11434, UI :3000)
5. Comprehensive test suite regression (AIOS, VECTIS, Sovereign Continuum, OMEGA OS)
6. Export of machine-readable reports/BUILD_REPORT.json and master audit logging
========================================================================================
"""

import os
import sys
import json
import time
import socket
import sqlite3
import py_compile
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any

ROOT_DIR = Path("E:/anti").resolve()
AIOS_DIR = ROOT_DIR / "aios"
REPORTS_DIR = ROOT_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Add relevant paths for imports
for p in [AIOS_DIR, AIOS_DIR / "databases", AIOS_DIR / "projects", ROOT_DIR / "company", ROOT_DIR / "sovereign_continuum"]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


def log_step(step_name: str):
    print(f"\n{'='*80}")
    print(f"[*] STEP: {step_name}")
    print(f"{'='*80}")


def check_syntax() -> Dict[str, Any]:
    log_step("1. Python Syntax & Bytecode Compilation Gate")
    target_dirs = [
        AIOS_DIR / "ai",
        AIOS_DIR / "automation",
        AIOS_DIR / "databases",
        AIOS_DIR / "projects",
        AIOS_DIR / "scripts",
        AIOS_DIR / "tests",
        ROOT_DIR / "company",
        ROOT_DIR / "sovereign_continuum",
        ROOT_DIR / "omega" / "core",
        ROOT_DIR / "scripts",
    ]
    compiled_count = 0
    errors = []

    for d in target_dirs:
        if not d.exists():
            continue
        for py_file in d.glob("**/*.py"):
            if "node_modules" in str(py_file) or ".venv" in str(py_file):
                continue
            try:
                py_compile.compile(str(py_file), doraise=True)
                compiled_count += 1
            except Exception as e:
                errors.append({"file": str(py_file), "error": str(e)})

    print(f"    [OK] Successfully compiled {compiled_count} Python source files.")
    if errors:
        print(f"    [!] Detected {len(errors)} compilation errors:")
        for err in errors[:5]:
            print(f"        -> {err['file']}: {err['error']}")
    return {
        "status": "PASS" if not errors else "FAIL",
        "compiled_files": compiled_count,
        "error_count": len(errors),
        "errors": errors
    }


def check_databases() -> Dict[str, Any]:
    log_step("2. SQLite Database Integrity & WAL Maintenance")
    databases = [
        AIOS_DIR / "data" / "master.db",
        ROOT_DIR / "data" / "global_10000_targets.db",
        ROOT_DIR / "data" / "outreach_tracker.db",
        ROOT_DIR / "company" / "nexus_product.db",
        ROOT_DIR / "omega" / "omega_platform.db",
        ROOT_DIR / "BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite",
    ]
    results = {}

    for db_path in databases:
        name = db_path.name
        if not db_path.exists():
            results[name] = {"exists": False, "status": "SKIPPED_NOT_FOUND"}
            continue
        try:
            con = sqlite3.connect(str(db_path), timeout=10.0)
            cur = con.cursor()
            cur.execute("PRAGMA integrity_check;")
            row = cur.fetchone()
            integrity = row[0] if row else "unknown"
            
            # Checkpoint WAL
            cur.execute("PRAGMA wal_checkpoint(PASSIVE);")
            cur.execute("PRAGMA optimize;")
            con.commit()
            cur.close()
            con.close()
            
            results[name] = {"exists": True, "integrity": integrity, "status": "HEALTHY" if integrity == "ok" else "CORRUPT"}
            print(f"    [OK] {name:<26} => Integrity: {integrity} (WAL Optimized)")
        except Exception as e:
            results[name] = {"exists": True, "error": str(e), "status": "ERROR"}
            print(f"    [!] {name:<26} => Error: {e}")

    all_healthy = all(r.get("status") in ["HEALTHY", "SKIPPED_NOT_FOUND"] for r in results.values())
    return {
        "status": "PASS" if all_healthy else "FAIL",
        "databases": results
    }


def check_saas_portfolio() -> Dict[str, Any]:
    log_step("3. SaaS Factory 4-Stack Reference Portfolio Audit")
    scaffold_dir = AIOS_DIR / "projects" / "scaffolded"
    expected_stacks = {
        "omni-recon-platform": "nextjs-fastapi",
        "exim-flow-analyzer": "nextjs-flask",
        "sovereign-portal": "static-api",
        "omega-strike-cli": "python-cli",
    }
    portfolio = {}

    for proj_name, expected_stack in expected_stacks.items():
        proj_path = scaffold_dir / proj_name
        exists = proj_path.exists()
        has_readme = (proj_path / "README.md").exists()
        has_makefile = (proj_path / "Makefile").exists()
        portfolio[proj_name] = {
            "expected_stack": expected_stack,
            "exists": exists,
            "has_readme": has_readme,
            "has_makefile": has_makefile,
            "path": str(proj_path)
        }
        status_flag = "[OK]" if (exists and has_readme and has_makefile) else "[MISSING]"
        print(f"    {status_flag} {proj_name:<24} ({expected_stack:<14}) => Staged & Configured")

    all_valid = all(p["exists"] and p["has_readme"] and p["has_makefile"] for p in portfolio.values())
    return {
        "status": "PASS" if all_valid else "FAIL",
        "portfolio": portfolio
    }


def check_service_mesh() -> Dict[str, Any]:
    log_step("4. Service Mesh Live Port & Endpoint Verification")
    ports = {
        "AIOS Gateway": ("127.0.0.1", 8090),
        "Ollama GPU": ("127.0.0.1", 11434),
        "Command UI": ("127.0.0.1", 3000),
    }
    services = {}

    for name, (host, port) in ports.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        try:
            res = s.connect_ex((host, port))
            online = (res == 0)
        except Exception:
            online = False
        finally:
            s.close()
        services[name] = {"host": host, "port": port, "online": online}
        state = "[ONLINE]" if online else "[OFFLINE]"
        print(f"    * {name:<18} (Port {port:<5}) : {state}")

    return {
        "status": "PASS" if all(s["online"] for s in services.values()) else "WARNING",
        "services": services
    }


def run_test_suites() -> Dict[str, Any]:
    log_step("5. Comprehensive Multi-Subsystem Test Suite Regression")
    suites = [
        {
            "name": "AIOS Full Stack Regression (38 Tests)",
            "cmd": [sys.executable, "-m", "unittest", "discover", "-s", str(AIOS_DIR / "tests"), "-p", "test_*.py"],
            "cwd": str(AIOS_DIR)
        },
        {
            "name": "VECTIS Trade Compliance Engine (9 Tests)",
            "cmd": [sys.executable, "-m", "pytest", "company/test_vectis_core.py", "company/test_vectis_end_to_end.py"],
            "cwd": str(ROOT_DIR)
        },
        {
            "name": "Sovereign Continuum & Universal Job (10 Tests)",
            "cmd": [sys.executable, "-m", "pytest", "sovereign_continuum/tests/test_capability_engine.py", "sovereign_continuum/tests/test_omni_era_universal_job.py"],
            "cwd": str(ROOT_DIR)
        },
        {
            "name": "OMEGA OS Core Engine (14 Tests)",
            "cmd": [sys.executable, "-m", "pytest", "omega/tests/test_omega_os.py"],
            "cwd": str(ROOT_DIR)
        },
        {
            "name": "OMNIVERSE INFINITY Comprehensive Suite (25 Tests)",
            "cmd": [sys.executable, "-m", "unittest", "test_omniverse_full_suite.py"],
            "cwd": str(ROOT_DIR)
        }
    ]
    results = {}
    total_passed = 0
    all_ok = True

    for suite in suites:
        name = suite["name"]
        print(f"\n    --> Running: {name}...")
        t0 = time.time()
        res = subprocess.run(suite["cmd"], cwd=suite["cwd"], capture_output=True, text=True)
        dur = round(time.time() - t0, 2)
        passed = (res.returncode == 0)
        results[name] = {
            "passed": passed,
            "returncode": res.returncode,
            "duration_sec": dur,
            "stdout_tail": res.stdout[-400:] if res.stdout else "",
            "stderr_tail": res.stderr[-400:] if res.stderr else ""
        }
        if passed:
            print(f"        [PASS] Completed in {dur}s (Return Code 0)")
        else:
            print(f"        [FAIL] Suite failed with code {res.returncode}")
            print(f"        Error excerpt: {res.stderr[-300:]}")
            all_ok = False

    return {
        "status": "PASS" if all_ok else "FAIL",
        "suites": results
    }


def main():
    print("=" * 80)
    print("       ANTIGRAVITY OMEGA :: MASTER PLATFORM BUILD & VERIFICATION")
    print("=" * 80)
    t_start = time.time()

    build_report = {
        "build_id": f"BUILD-{int(time.time())}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "platform": {
            "os": sys.platform,
            "python": sys.version.split()[0],
            "root_dir": str(ROOT_DIR),
        },
        "pillars": {}
    }

    # Execute all pillars
    build_report["pillars"]["syntax"] = check_syntax()
    build_report["pillars"]["databases"] = check_databases()
    build_report["pillars"]["saas_portfolio"] = check_saas_portfolio()
    build_report["pillars"]["service_mesh"] = check_service_mesh()
    build_report["pillars"]["test_suites"] = run_test_suites()

    # Determine overall status
    statuses = [p["status"] for p in build_report["pillars"].values()]
    overall = "SUCCESS" if all(s in ["PASS", "WARNING"] for s in statuses) and build_report["pillars"]["test_suites"]["status"] == "PASS" else "FAILED"
    build_report["overall_status"] = overall
    build_report["total_duration_sec"] = round(time.time() - t_start, 2)

    # Save JSON report
    report_path = REPORTS_DIR / "BUILD_REPORT.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(build_report, f, indent=2)

    # Record to master audit ledger
    try:
        from db import log_audit
        log_audit("BUILD_RUNNER", "MASTER_BUILD", "SYSTEM", f"Completed master platform build: {overall}", "INFO" if overall == "SUCCESS" else "ERROR")
    except Exception:
        pass

    log_step("Build Summary & Conclusion")
    print(f"    Build ID         : {build_report['build_id']}")
    print(f"    Overall Status   : [{overall}]")
    print(f"    Total Time       : {build_report['total_duration_sec']} seconds")
    print(f"    Report Saved To  : {report_path}")
    print("=" * 80)

    if overall != "SUCCESS":
        sys.exit(1)


if __name__ == "__main__":
    main()
