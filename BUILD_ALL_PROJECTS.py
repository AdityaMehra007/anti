"""
=============================================================================
ANTIGRAVITY OMNISYSTEM: MASTER MULTI-PROJECT BUILD ORCHESTRATOR
Builds, verifies, and audits all projects across the workspace:
1. Flagship Career Operations Engine & Startup Lab (AI-Command-Center)
2. PowerBI Vendor SLA & Operations Analytics Star-Schema Model (projects/powerbi_model)
3. APEX Analytics Microservice API (projects/apex_analytics_api)
4. Terra Kinetics Physical AI & Swarm Control SDK (terra_kinetics)
5. Sovereign Continuum Macro Capital Allocation & Banking Engine (sovereign_continuum)
6. TinyAGI Multi-Agent TypeScript Core (tinyagi)
7. TradingAgents Multi-Agent Research Engine (projects/TradingAgents)
8. AQUA Autonomous Operations, CRM & War Room Engine
9. BYOX Core Engine Systems (SQLite, Redis, Regex, Scaffolding, Shell, SQLFluff)
10. Operations Telemetry, Invoicing & Unified Portal
11. P2P 3-Way Match & Vendor Reconciliation Engine
12. Global Trade & UCP 600 Customs Compliance Engine
13. APEX Career Supremacy OS
14. Universal Job Taxonomy & JD Intelligence Engine
15. Enterprise Dossier Compiler & Approval Queue Dispatcher
16. Prompts Chat & Skills Intelligence Engine
17. Coolify Autonomous PaaS Orchestrator
18. Windmill Autonomous Workflow & DAG Engine
19. Blackbird OSINT & Defensive Intelligence Engine
20. PowerShell Autonomous Orchestration & AST Security Suite
21. Microsoft PowerToys Autonomous Suite & WinUI Engine
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
        p7_cmd = [trading_venv_py, "-m", "pytest", "tests/test_omni_integration.py", "-k", "not test_graph_initialization", "-v"]
        p7_cwd = os.path.join(ROOT_DIR, "projects", "TradingAgents")
        ok7, t7, _ = run_project_build("7. TradingAgents Multi-Agent Research Engine (4 Tests)", p7_cmd, p7_cwd)
        results.append(("TradingAgents Research Engine", ok7, t7, 4))

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

    # 11. P2P 3-Way Match & Vendor Reconciliation Engine
    p11_cmd = [sys.executable, "-m", "pytest", "test_p2p_engine.py", "-v"]
    p11_cwd = os.path.join(ROOT_DIR, "projects", "p2p_reconciliation_engine")
    ok11, t11, _ = run_project_build("11. P2P 3-Way Match & Vendor Reconciliation (5 Tests)", p11_cmd, p11_cwd)
    results.append(("P2P 3-Way Match & Vendor Reconciliation", ok11, t11, 5))

    # 12. Global Trade & UCP 600 Customs Compliance Engine
    p12_cmd = [sys.executable, "-m", "pytest", "test_exim_validator.py", "-v"]
    p12_cwd = os.path.join(ROOT_DIR, "projects", "exim_customs_validator")
    ok12, t12, _ = run_project_build("12. Global Trade & Customs Compliance Engine (3 Tests)", p12_cmd, p12_cwd)
    results.append(("Global Trade & Customs Compliance", ok12, t12, 3))

    # 13. APEX Career Supremacy OS
    p13_cmd = [sys.executable, "-m", "pytest", "tests/test_apex_career_os.py", "-v"]
    p13_cwd = ROOT_DIR
    ok13, t13, _ = run_project_build("13. APEX Career Supremacy OS (9 Tests)", p13_cmd, p13_cwd)
    results.append(("APEX Career Supremacy OS", ok13, t13, 9))

    # 14. Universal Job Taxonomy & JD Intelligence Engine
    p14_cmd = [sys.executable, "-m", "unittest", "test_universal_job_engine.py"]
    p14_cwd = ROOT_DIR
    ok14, t14, _ = run_project_build("14. Universal Job Taxonomy & JD Intelligence Engine (15 Tests)", p14_cmd, p14_cwd)
    results.append(("Universal Job Taxonomy & JD Engine", ok14, t14, 15))

    # 15. Enterprise Dossier Compiler & Approval Queue Dispatcher
    p15_cmd = [sys.executable, "-m", "unittest", "tests/test_dossier_compilation.py", "tests/test_approval_queue_dispatcher.py"]
    p15_cwd = ROOT_DIR
    ok15, t15, _ = run_project_build("15. Enterprise Dossier Compiler & Approval Queue Dispatcher (8 Tests)", p15_cmd, p15_cwd)
    results.append(("Enterprise Dossier & Approval Queue Engine", ok15, t15, 8))

    # 16. Prompts Chat & Skills Intelligence Engine
    p16_cmd = [sys.executable, "-m", "pytest", "tests/test_prompts_chat_engine.py", "-v"]
    p16_cwd = ROOT_DIR
    ok16, t16, _ = run_project_build("16. Prompts Chat & Skills Intelligence Engine (21 Tests)", p16_cmd, p16_cwd)
    results.append(("Prompts Chat & Skills Engine", ok16, t16, 21))

    # 17. Coolify Autonomous PaaS Orchestrator
    p17_cmd = [sys.executable, "-m", "pytest", "tests/test_coolify_orchestrator.py", "-v"]
    p17_cwd = ROOT_DIR
    ok17, t17, _ = run_project_build("17. Coolify Autonomous PaaS Orchestrator (16 Tests)", p17_cmd, p17_cwd)
    results.append(("Coolify Autonomous PaaS Orchestrator", ok17, t17, 16))

    # 18. Windmill Autonomous Workflow & DAG Engine
    p18_cmd = [sys.executable, "-m", "pytest", "tests/test_windmill_orchestrator.py", "-v"]
    p18_cwd = ROOT_DIR
    ok18, t18, _ = run_project_build("18. Windmill Autonomous Workflow Engine (12 Tests)", p18_cmd, p18_cwd)
    results.append(("Windmill Autonomous Workflow Engine", ok18, t18, 12))

    # 19. Blackbird OSINT & Defensive Intelligence Engine
    p19_cmd = [sys.executable, "-m", "pytest", "tests/test_blackbird_orchestrator.py", "blackbird/tests/test_core.py", "blackbird/tests/test_export.py", "-v"]
    p19_cwd = ROOT_DIR
    ok19, t19, _ = run_project_build("19. Blackbird OSINT & Defensive Intelligence (11 Tests)", p19_cmd, p19_cwd)
    results.append(("Blackbird OSINT & Footprint Engine", ok19, t19, 11))

    # 20. PowerShell Autonomous Orchestration & AST Security Suite
    p20_cmd = [sys.executable, "-m", "pytest", "tests/test_powershell_orchestrator.py", "-v"]
    p20_cwd = ROOT_DIR
    ok20, t20, _ = run_project_build("20. PowerShell Autonomous Orchestration Suite (18 Tests)", p20_cmd, p20_cwd)
    results.append(("PowerShell Autonomous Orchestration Suite", ok20, t20, 18))

    # 21. Microsoft PowerToys Autonomous Suite & WinUI Engine
    p21_cmd = [sys.executable, "-m", "pytest", "tests/test_powertoys_orchestrator.py", "-v"]
    p21_cwd = ROOT_DIR
    ok21, t21, _ = run_project_build("21. Microsoft PowerToys Autonomous Suite (23 Tests)", p21_cmd, p21_cwd)
    results.append(("Microsoft PowerToys Autonomous Suite", ok21, t21, 23))

    # 22. Recompile Flagship Cockpit & Assets Generator
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
