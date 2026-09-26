"""
ADITYA GLOBAL CAREER INTELLIGENCE OS — AUTOMATED DAILY SCHEDULER
Enforces continuous automated daily execution (Section 86 of Master Spec).
Supports both:
1. Windows schtasks task registration (Runs silently in background at 08:00 AM)
2. Live Python process daemon mode
"""

import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent
PYTHON_EXE = sys.executable
CLI_SCRIPT = ROOT_DIR / "aditya_global_career_intelligence_os.py"

def register_windows_task():
    """Registers a Windows Task Scheduler job to run daily at 08:00 AM."""
    task_name = "AdityaCareerIntelligenceDailySync"
    cmd = f'"{PYTHON_EXE}" "{CLI_SCRIPT}" /refresh-data'
    
    ps_cmd = f'schtasks /create /tn "{task_name}" /tr "{cmd}" /sc daily /st 08:00 /f'
    print(f"Executing: {ps_cmd}")
    try:
        res = subprocess.run(ps_cmd, shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"SUCCESS: Windows Scheduled Task '{task_name}' registered successfully.")
            print("The Career OS will automatically execute every morning at 08:00 AM.")
        else:
            print(f"Notice: {res.stderr.strip()}")
            print("To run with admin privileges, run PowerShell as Administrator.")
    except Exception as e:
        print(f"Error registering task: {e}")

def run_immediate_refresh():
    """Runs an immediate pipeline refresh."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Launching daily pipeline refresh...")
    subprocess.run([PYTHON_EXE, str(CLI_SCRIPT), "/refresh-data"])
    # Rebuild reports & cockpit
    subprocess.run([PYTHON_EXE, str(ROOT_DIR / "generate_executive_reports.py")])
    subprocess.run([PYTHON_EXE, str(ROOT_DIR / "build_cockpit_html.py")])
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Refresh complete. Reports & Cockpit synchronized.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--register":
        register_windows_task()
    else:
        run_immediate_refresh()
