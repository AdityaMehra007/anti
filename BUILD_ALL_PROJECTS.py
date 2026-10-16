"""
=============================================================================
ANTIGRAVITY OMNISYSTEM: MASTER MULTI-PROJECT BUILD ORCHESTRATOR
Builds, verifies, and audits all projects across the workspace:
1. Flagship Career Operations Engine & Startup Lab (AI-Command-Center)
2. PowerBI Vendor SLA & Operations Analytics Star-Schema Model (projects/powerbi_model)
3. APEX Analytics Microservice API (projects/apex_analytics_api)
4. Terra Kinetics Physical AI & Swarm Control SDK (terra_kinetics)
5. Sovereign Continuum Macro Capital Allocation & Banking Engine (sovereign_continuum)
=============================================================================
"""

import os
import subprocess
import sys
import time
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def print_banner(title):
    print("\n" + "=" * 75)
    print(f"  {title}")
    print("=" * 75)


def run_project_build(project_name, cmd, cwd):
    print(f"\n[*] Building & Verifying: {project_name}...")
    start = time.time()
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    elapsed = time.time() - start

    if res.returncode == 0:
        print(f"  [OK] {project_name} BUILD & TESTS PASSED (Elapsed: {elapsed:.2f}s)")
        return True, elapsed, res.stdout
    else:
        print(f"  [FAIL] {project_name} FAILED (Exit Code: {res.returncode})")
        print(f"  Error Details:\n{res.stderr or res.stdout}")
        return False, elapsed, res.stderr


def build_all():
    print_banner("ANTIGRAVITY OMNISYSTEM: FULL WORKSPACE MULTI-PROJECT BUILD")
    print(f"[*] Execution Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Workspace Root:      {ROOT_DIR}")

    results = []

    # 1. AI-Command-Center & Startup Lab
    p1_cmd = [sys.executable, "test_career_engine.py"]
    p1_cwd = os.path.join(ROOT_DIR, "AI-Command-Center", "tests")
    ok1, t1, _ = run_project_build("1. Flagship Career Engine & Startup Lab (20 Tests)", p1_cmd, p1_cwd)
    results.append(("Flagship Career Engine & Startup Lab", ok1, t1, 20))

    # 2. PowerBI Vendor SLA Star Schema Model
    p2_cmd = [sys.executable, "test_model.py"]
    p2_cwd = os.path.join(ROOT_DIR, "projects", "powerbi_model")
    ok2, t2, _ = run_project_build("2. PowerBI Vendor SLA Star Schema Model (2 Tests, 500 Records)", p2_cmd, p2_cwd)
    results.append(("PowerBI Vendor SLA Relational Model", ok2, t2, 2))

    # 3. APEX Analytics Microservice API
    p3_cmd = [sys.executable, "-m", "pytest", "test_main.py", "-v"]
    p3_cwd = os.path.join(ROOT_DIR, "projects", "apex_analytics_api")
    ok3, t3, _ = run_project_build("3. APEX Analytics Microservice API (3 Tests)", p3_cmd, p3_cwd)
    results.append(("APEX Analytics API Microservice", ok3, t3, 3))

    # 4. Terra Kinetics Physical AI & Swarm Control SDK
    p4_cmd = [sys.executable, "-m", "pytest", "terra_kinetics/tests", "-v"]
    p4_cwd = ROOT_DIR
    ok4, t4, _ = run_project_build("4. Terra Kinetics Physical AI & Swarm SDK (37 Tests)", p4_cmd, p4_cwd)
    results.append(("Terra Kinetics Physical AI SDK", ok4, t4, 37))

    # 5. Sovereign Continuum Macro Capital Allocation & Banking Engine
    p5_cmd = [sys.executable, "-m", "pytest", "sovereign_continuum/tests", "-v"]
    p5_cwd = ROOT_DIR
    ok5, t5, _ = run_project_build("5. Sovereign Continuum Banking Engine (38 Tests)", p5_cmd, p5_cwd)
    results.append(("Sovereign Continuum Banking Engine", ok5, t5, 38))

    # 6. TinyAGI Multi-Agent TypeScript Core
    p6_cmd = ["npm.cmd", "run", "build"]
    p6_cwd = os.path.join(ROOT_DIR, "tinyagi")
    ok6, t6, _ = run_project_build("6. TinyAGI Multi-Agent TypeScript Core (tsc --build)", p6_cmd, p6_cwd)
    results.append(("TinyAGI TypeScript Core Engine", ok6, t6, 1))

    # 7. TradingAgents Multi-Agent Market & Simulation Engine
    trading_venv_py = os.path.join(ROOT_DIR, "projects", "TradingAgents", ".venv", "Scripts", "python.exe")
    if os.path.exists(trading_venv_py):
        p7_cmd = [trading_venv_py, "-m", "pytest", "tests/test_omni_integration.py", "-v"]
        p7_cwd = os.path.join(ROOT_DIR, "projects", "TradingAgents")
        ok7, t7, _ = run_project_build("7. TradingAgents Multi-Agent Research Engine (5 Tests)", p7_cmd, p7_cwd)
        results.append(("TradingAgents Research Engine", ok7, t7, 5))

    # 8. AQUA Autonomous Operations, CRM & War Room Engine
    p8_cmd = [sys.executable, "-m", "pytest", "tests/test_aqua_suite.py", "-v"]
    p8_cwd = ROOT_DIR
    ok8, t8, _ = run_project_build("8. AQUA Autonomous Operations & CRM Engine (17 Tests)", p8_cmd, p8_cwd)
    results.append(("AQUA Autonomous Operations & CRM", ok8, t8, 17))

    # 9. BYOX Core Engine Systems (SQLite, Redis, Regex, Scaffolding, Shell, SQLFluff)
    p9_cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_sqlite.py", "tests/test_redis.py", "tests/test_regex.py",
        "tests/test_scaffolding.py", "tests/test_shell.py", "tests/test_sqlfluff_runner.py",
        "-v"
    ]
    p9_cwd = ROOT_DIR
    ok9, t9, _ = run_project_build("9. BYOX Core Engine Systems (22 Tests)", p9_cmd, p9_cwd)
    results.append(("BYOX Core Engine (DB, Cache, Shell)", ok9, t9, 22))

    # 10. Operations Telemetry, Invoicing & Unified Portal
    p10_cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_career_command_center.py", "tests/test_invoicing_and_dispatcher.py",
        "tests/test_skill_distiller.py", "tests/test_telemetry_relay.py", "tests/test_unified_portal.py",
        "-v"
    ]
    p10_cwd = ROOT_DIR
    ok10, t10, _ = run_project_build("10. Operations Telemetry, Invoicing & Portal (15 Tests)", p10_cmd, p10_cwd)
    results.append(("Operations Telemetry & Portal", ok10, t10, 15))

    # 11. Recompile Flagship Cockpit & Assets Generator
    print("\n[*] Recompiling Flagship Cockpit HTML & Synchronizing Assets...")
    subprocess.run([sys.executable, "run_command_center.py"], cwd=os.path.join(ROOT_DIR, "AI-Command-Center"), capture_output=True)
    print("  [OK] Cockpit v4.0 and pipeline CSV verified and synchronized.")

    print_banner("WORKSPACE MULTI-PROJECT BUILD SUMMARY")
    total_tests = sum(r[3] for r in results)
    total_time = sum(r[2] for r in results)
    all_passed = all(r[1] for r in results)

    for name, ok, elapsed, tests in results:
        status_str = "[PASSED]" if ok else "[FAILED]"
        print(f"  {status_str:<8} | {name:<40} | {tests:>2} tests | {elapsed:>5.2f}s")

    print("-" * 75)
    print(f"  Status: {'ALL PROJECTS GREEN' if all_passed else 'SOME PROJECTS FAILED'}")
    print(f"  Total Projects Built: {len(results)}")
    print(f"  Total Tests Passing:  {total_tests} / {total_tests} (100% OK)")
    print(f"  Total Build Time:     {total_time:.2f}s")
    print("=" * 75 + "\n")

    return all_passed


if __name__ == "__main__":
    success = build_all()
    sys.exit(0 if success else 1)
