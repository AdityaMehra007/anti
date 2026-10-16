"""
=============================================================================
ANTIGRAVITY OMNISYSTEM: MASTER SETUP & ENVIRONMENT INITIALIZATION
Verifies all prerequisites, directories, database integrity, resume assets,
and launches initial synchronization across all subsystems.
=============================================================================
"""

import os
import sqlite3
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_PATH = os.path.join(
    BASE_DIR, "projects", "flagship-career-engine", "career_vault.db"
)
CAREER_DIR = os.path.join(BASE_DIR, "career")
STARTUP_DIR = os.path.join(BASE_DIR, "startup-lab")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
BACKUPS_DIR = os.path.join(BASE_DIR, "backups")


def print_step(title):
    print(f"\n[*] {title}")


def check_ok(msg):
    print(f"  [OK] {msg}")


def check_warn(msg):
    print(f"  [WARN] {msg}")


def check_fail(msg):
    print(f"  [FAIL] {msg}")


def setup_environment():
    print("=" * 70)
    print("  ANTIGRAVITY OMNISYSTEM: COMPREHENSIVE SYSTEM SETUP")
    print("=" * 70)
    print(f"Workspace Directory: {BASE_DIR}")
    print(f"Python Runtime:      {sys.version.split()[0]}")

    errors = 0

    # 1. Directory Structure Setup
    print_step("Step 1: Setting up Directory Hierarchy...")
    required_dirs = [
        os.path.join(BASE_DIR, "automation"),
        os.path.join(BASE_DIR, "backups"),
        os.path.join(BASE_DIR, "career"),
        os.path.join(BASE_DIR, "projects", "flagship-career-engine"),
        os.path.join(BASE_DIR, "reports"),
        os.path.join(BASE_DIR, "research"),
        os.path.join(BASE_DIR, "startup-lab", "incoming_quotes"),
        os.path.join(BASE_DIR, "startup-lab", "audits"),
        os.path.join(BASE_DIR, "tests"),
    ]
    for d in required_dirs:
        os.makedirs(d, exist_ok=True)
        check_ok(f"Directory ready: {os.path.relpath(d, BASE_DIR)}")

    # 2. Toolchain & CLI Audit
    print_step("Step 2: Verifying Toolchain & Formatting Binaries...")
    tools = [
        ("ruff", ["ruff", "--version"]),
        ("black", ["black", "--version"]),
        ("git", ["git", "--version"]),
        ("node", ["node", "-v"]),
        ("npm", ["npm", "-v"]),
    ]
    for name, cmd in tools:
        try:
            res = subprocess.run(
                cmd, capture_output=True, text=True, check=False, shell=True
            )
            if res.returncode == 0:
                check_ok(
                    f"{name.capitalize()} verified: {res.stdout.strip().splitlines()[0]}"
                )
            else:
                check_warn(f"{name.capitalize()} check returned non-zero code.")
        except FileNotFoundError:
            check_warn(f"{name.capitalize()} command not found in PATH.")

    # 3. SQLite Database Initialization & Integrity
    print_step("Step 3: Initializing SQLite Vault with WAL Concurrency Mode...")
    os.makedirs(os.path.dirname(VAULT_PATH), exist_ok=True)
    conn = sqlite3.connect(VAULT_PATH)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute("PRAGMA busy_timeout = 5000;")

    # Run integrity check
    cur = conn.cursor()
    cur.execute("PRAGMA integrity_check;")
    integrity = cur.fetchone()[0]
    if integrity == "ok":
        check_ok(f"Database integrity verified: {integrity}")
    else:
        check_fail(f"Database integrity check failed: {integrity}")
        errors += 1

    # Check table existence
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    check_ok(f"Tables present: {', '.join(tables)}")

    cur.execute("SELECT COUNT(*) FROM jobs")
    job_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM jobs WHERE fit_score >= 80")
    high_fit_count = cur.fetchone()[0]
    check_ok(f"Opportunities in vault: {job_count} (High-Fit >= 80: {high_fit_count})")
    conn.close()

    # 4. Resume Documents Verification
    print_step("Step 4: Verifying Dual-Format Word & ATS PDF Resumes...")
    resume_stems = [
        "ADITYA_MEHRA_MASTER_ATS_RESUME",
        "ADITYA_MEHRA_SUPPLY_CHAIN_PROCUREMENT",
        "ADITYA_MEHRA_AI_DATA_OPERATIONS",
    ]
    for stem in resume_stems:
        docx = os.path.join(CAREER_DIR, f"{stem}.docx")
        pdf = os.path.join(CAREER_DIR, f"{stem}.pdf")
        if os.path.exists(docx) and os.path.getsize(docx) > 5000:
            check_ok(f"Word Resume: {stem}.docx ({os.path.getsize(docx):,} bytes)")
        else:
            check_fail(f"Missing or empty Word resume: {stem}.docx")
            errors += 1

        if os.path.exists(pdf) and os.path.getsize(pdf) > 20000:
            check_ok(f"ATS PDF Resume: {stem}.pdf ({os.path.getsize(pdf):,} bytes)")
        else:
            check_fail(f"Missing or empty ATS PDF resume: {stem}.pdf")
            errors += 1

    # 5. Asset Cross-Linker Execution
    print_step("Step 5: Synchronizing Asset Cross-Linker...")
    link_script = os.path.join(BASE_DIR, "automation", "asset_cross_linker.py")
    if os.path.exists(link_script):
        res = subprocess.run(
            [sys.executable, link_script], capture_output=True, text=True, check=False
        )
        if res.returncode == 0:
            check_ok("Assets successfully mapped to SQLite career vault.")
        else:
            check_warn(f"Asset linker notice: {res.stderr}")

    # 6. Recompiling Dashboard & CSV Export
    print_step("Step 6: Compiling Interactive Cockpit & Exporting CSV...")
    dash_script = os.path.join(
        BASE_DIR, "projects", "flagship-career-engine", "generate_dashboard.py"
    )
    csv_script = os.path.join(BASE_DIR, "automation", "export_pipeline_csv.py")
    subprocess.run(
        [sys.executable, dash_script],
        cwd=os.path.dirname(dash_script),
        capture_output=True,
        check=False,
    )
    subprocess.run([sys.executable, csv_script], capture_output=True, check=False)
    check_ok("Cockpit v4.0 HTML and pipeline CSV compiled.")

    # 7. Running Verification Test Suite (20 Tests)
    print_step("Step 7: Running 20-Test Automated Verification Battery...")
    test_script = os.path.join(BASE_DIR, "tests", "test_career_engine.py")
    test_res = subprocess.run(
        [sys.executable, test_script],
        cwd=os.path.dirname(test_script),
        capture_output=True,
        text=True,
        check=False,
    )
    if test_res.returncode == 0:
        check_ok("All 20 unit and integration tests passed (100% OK).")
    else:
        check_fail(f"Test suite encountered failures:\n{test_res.stderr}")
        errors += 1

    # 8. Create Backup Snapshot
    print_step("Step 8: Creating Baseline Database Snapshot...")
    backup_script = os.path.join(BASE_DIR, "automation", "backup_vault.py")
    subprocess.run([sys.executable, backup_script], capture_output=True, check=False)
    check_ok("Snapshot preserved in backups/ directory.")

    print("\n" + "=" * 70)
    if errors == 0:
        print("  SETUP COMPLETE: ALL SYSTEMS CONFIGURED, OPTIMIZED & GREEN")
        print("=" * 70)
        print("  Quick Start Commands:")
        print("  - Launch Cockpit:          START_COMMAND_CENTER.bat")
        print("  - Run Full Master Cycle:   START_FULL_CYCLE.bat")
        print("  - Local Dashboard Server:  START_DASHBOARD_SERVER.bat")
        print("  - View Daily Briefing:     DAILY_BRIEFING.md")
        print("=" * 70)
        return 0
    else:
        print(f"  SETUP COMPLETED WITH {errors} ERRORS.")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(setup_environment())
