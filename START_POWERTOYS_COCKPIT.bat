@echo off
title Microsoft PowerToys Mission Control Cockpit Bridge
color 0a
echo ===============================================================================
echo   STARTING POWERTOYS AUTONOMOUS API BRIDGE & MISSION CONTROL COCKPIT
echo ===============================================================================
echo.
echo Starting Local REST Bridge on port 8770...
start "" "http://localhost:8770/cockpit"
python powertoys_api_server.py --port 8770
pause
