@echo off
title NSA Ghidra Autonomous Mission Control Cockpit
color 0a
echo ===============================================================================
echo   NSA GHIDRA AUTONOMOUS MISSION CONTROL COCKPIT (Port 8770)
echo ===============================================================================
echo.
echo Launching NSA Ghidra Autonomous API Server on port 8771...
start "" http://localhost:8771/
python ghidra_api_server.py --port 8771
pause
