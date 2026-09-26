@echo off
TITLE Antigravity 24/7/365 Autonomous Career Autopilot Daemon
COLOR 0B
echo ================================================================================
echo         ?? ANTIGRAVITY 24/7/365 AUTONOMOUS CAREER AUTOPILOT DAEMON
echo ================================================================================
echo Candidate: Aditya Mehra | BBA International Business (Dayananda Sagar Univ)
echo Status: Continuous Background Operation Active
echo ================================================================================
echo.

:loop
set PYTHONIOENCODING=utf-8
python -c "
import sys, os
sys.path.insert(0, r'e:\anti')
import master_career_autopilot_daemon
master_career_autopilot_daemon.run_autopilot_cycle()
"
echo.
echo [STANDBY] Sleeping for 3600 seconds (1 hour) before next cycle...
timeout /t 3600 /nobreak >nul
goto loop
