@echo off
title PowerShell Autonomous Mission Control Cockpit
color 0b
echo ===============================================================================
echo   POWERSHELL AUTONOMOUS MISSION CONTROL COCKPIT (github.com/PowerShell/PowerShell)
echo ===============================================================================
echo.
echo Launching PowerShell Autonomous API Server on port 8769...
start "" http://localhost:8769/
python powershell_api_server.py --port 8769
pause
