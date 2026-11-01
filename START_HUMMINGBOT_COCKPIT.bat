@echo off
title Hummingbot Mission Control Cockpit Bridge
color 0a
echo ===============================================================================
echo   STARTING HUMMINGBOT AUTONOMOUS API BRIDGE & MISSION CONTROL COCKPIT
echo ===============================================================================
echo.
echo Starting Local REST Bridge on port 8781...
start "" "http://localhost:8781/cockpit"
python hummingbot_api_server.py --port 8781
pause
