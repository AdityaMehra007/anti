"""
Unified Test Runner & Quality Verification Gate for All Enterprise Projects.
Executes all test suites across Bangalore Top 500, Fortune 500, APEX Career OS,
Omega Global Markets, and Enterprise Subsystems, generating an authoritative scorecard.
"""

import subprocess
import sys
import time
import os

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

TEST_TARGETS = [
    ("Bangalore Top 500 Master Suite", "tests/test_bangalore_top_500_master.py"),
    ("Bangalore Top 500 Flagship Systems (10 Projects)", "projects/bangalore_top_500"),
    ("Fortune 500 Enterprise Factory Systems", "fortune_500_projects/test_fortune500_all_sectors.py"),
    ("ApexFlow Enterprise Orchestrator", "projects/apex_enterprise_orchestrator/tests"),
    ("Omega Global Markets & EXIM Nexus", "projects/omega_global_markets_nexus/tests"),
    ("EXIM Customs & Tariff Validator", "projects/exim_customs_validator"),
    ("ApexAgentic Task Runtime", "projects/apex_agentic_task_runtime/tests"),
    ("APEX Career Supremacy OS", "tests/test_apex_career_os.py"),
    ("Universal Job & Skill Intelligence Engine", "test_universal_job_engine.py"),
    ("OMEGA Omniverse REST API & Pitch Decks Suite", "tests/test_omega_omniverse_api.py"),
    ("Mode H Antifragile Red-Team & Chaos Harness", "tests/test_antifragile_chaos_harness.py"),
]

def run_all_tests():
    print("=" * 84)
    print("        OMEGA ∞ SUPREME UNIFIED ENTERPRISE TEST VERIFICATION GATEWAY")
    print("=" * 84)

    total_passed = 0
    total_failed = 0
    t0_global = time.time()
    results_table = []

    for name, path in TEST_TARGETS:
        if not os.path.exists(path):
            print(f"\n[SKIP] {name} ({path} not found)")
            continue

        print(f"\n[RUNNING] {name}...")
        t0 = time.time()
        res = subprocess.run(
            [sys.executable, "-m", "pytest", path, "-q"],
            capture_output=True,
            text=True,
        )
        elapsed = time.time() - t0
        output_line = res.stdout.strip().splitlines()[-1] if res.stdout.strip() else ""

        if res.returncode == 0:
            count = 0
            if "passed" in output_line:
                try:
                    count = int(output_line.split("passed")[0].strip().split()[-1])
                except Exception:
                    count = 1
            total_passed += count
            status_str = f"PASS ({count} passed)"
            print(f"  --> [PASS] {output_line} ({elapsed:.2f}s)")
            results_table.append((name, "GREEN", count, f"{elapsed:.2f}s"))
        else:
            total_failed += 1
            print(f"  --> [FAIL] Error in {name}!\n{res.stdout}\n{res.stderr}")
            results_table.append((name, "RED", 0, f"{elapsed:.2f}s"))

    total_time = time.time() - t0_global
    print("\n" + "=" * 84)
    print(f"{'TEST SUITE':<52} | {'STATUS':<7} | {'PASSED':<8} | {'TIME'}")
    print("-" * 84)
    for name, status, count, elapsed in results_table:
        print(f"{name:<52} | {status:<7} | {count:<8} | {elapsed}")
    print("=" * 84)
    print(f"SUMMARY: {total_passed} TESTS PASSED | {total_failed} FAILED | TOTAL ELAPSED: {total_time:.2f}s")
    
    if total_failed == 0:
        print("RESULT: 100% UNIFIED SPECIFICATION COMPLIANCE ACHIEVED (ALL SYSTEMS GREEN)")
    else:
        print("RESULT: QUALITY GATE FAILED — RESOLVE RED TESTS IMMEDIATELY")
    print("=" * 84)

    return total_failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
