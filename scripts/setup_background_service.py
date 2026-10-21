#!/usr/bin/env python3
"""
setup_background_service.py - Windows Task Scheduler & Autonomous Daemon Manager
================================================================================
Registers and monitors the 24/7 background service for AUTONOMOUS_DAILY_ECOSYSTEM.py.
Enforces OMEGA Constitution Directives 10-14 (24/7 Perpetual Execution & Resilience).
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os
import subprocess
import argparse
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
SCRIPT_PATH = ROOT_DIR / "AUTONOMOUS_DAILY_ECOSYSTEM.py"
PYTHON_EXE = sys.executable
TASK_NAME = "OMEGA_Autonomous_Daily_Ecosystem"

def check_task_status():
    """Checks if the scheduled task exists in Windows Task Scheduler."""
    cmd = ["schtasks", "/query", "/tn", TASK_NAME, "/fo", "LIST"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"✅ Windows Scheduled Task '{TASK_NAME}' is registered and active:")
        for line in res.stdout.strip().split("\n")[:8]:
            print(f"   {line.strip()}")
        return True
    else:
        print(f"⚪ Windows Scheduled Task '{TASK_NAME}' is not yet registered.")
        return False

def register_scheduled_task(start_time="06:00"):
    """Registers a daily task in Windows Task Scheduler."""
    tr_command = f'"{PYTHON_EXE}" "{SCRIPT_PATH}" --once'
    cmd = [
        "schtasks", "/create",
        "/tn", TASK_NAME,
        "/tr", tr_command,
        "/sc", "DAILY",
        "/st", start_time,
        "/f"
    ]
    print(f"[*] Registering scheduled task '{TASK_NAME}' at {start_time} daily...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"✅ Successfully registered '{TASK_NAME}'! Output:\n   {res.stdout.strip()}")
        return True
    else:
        print(f"❌ Failed to register task: {res.stderr.strip()}")
        print(f"💡 Note: Registering Windows scheduled tasks may require Run as Administrator.")
        return False

def unregister_scheduled_task():
    """Deletes the scheduled task."""
    cmd = ["schtasks", "/delete", "/tn", TASK_NAME, "/f"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"✅ Successfully unregistered '{TASK_NAME}'.")
        return True
    else:
        print(f"Notice: {res.stderr.strip()}")
        return False

def create_daemon_launcher():
    """Creates a resilient Windows batch runner for running as an interactive or minimized daemon."""
    bat_path = ROOT_DIR / "START_AUTONOMOUS_DAEMON.bat"
    content = f"""@echo off
title OMEGA AUTONOMOUS DAILY ECOSYSTEM DAEMON
cd /d "{ROOT_DIR}"
echo ==============================================================================
echo   ANTIGRAVITY OMEGA: 24/7 AUTONOMOUS DAILY ECOSYSTEM DAEMON
echo   Interval: 24.0 Hours | Mode: Perpetual Autonomous Execution
echo ==============================================================================
:loop
echo [%date% %time%] Launching Autonomous Daily Ecosystem cycle...
"{PYTHON_EXE}" "{SCRIPT_PATH}" --once
if %errorlevel% neq 0 (
    echo [!] Warning: Cycle finished with exit code %errorlevel%. Pausing 60s before retry...
    timeout /t 60 /nobreak >nul
) else (
    echo [*] Cycle completed successfully. Sleeping for 24 hours (86,400 seconds)...
    timeout /t 86400 /nobreak >nul
)
goto loop
"""
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Generated resilient daemon launcher at:\n   {bat_path}")
    return bat_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OMEGA Background Service & Scheduler Setup")
    parser.add_argument("--status", action="store_true", help="Check status of scheduled task")
    parser.add_argument("--register", action="store_true", help="Register daily task in Windows Task Scheduler")
    parser.add_argument("--time", type=str, default="06:00", help="Time for daily execution (HH:MM, default 06:00)")
    parser.add_argument("--unregister", action="store_true", help="Unregister scheduled task")
    parser.add_argument("--generate-daemon", action="store_true", help="Generate START_AUTONOMOUS_DAEMON.bat")
    args = parser.parse_args()

    if args.register:
        register_scheduled_task(start_time=args.time)
        create_daemon_launcher()
    elif args.unregister:
        unregister_scheduled_task()
    elif args.generate_daemon:
        create_daemon_launcher()
    else:
        check_task_status()
        create_daemon_launcher()
