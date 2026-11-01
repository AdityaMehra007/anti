@echo off
title Hummingbot Mission Control Cockpit Bridge
color 0a
echo ===============================================================================
echo   STARTING HUMMINGBOT AUTONOMOUS API BRIDGE & MISSION CONTROL COCKPIT
echo ===============================================================================
echo.
echo Starting Local REST Bridge on port 8780...
start "" "http://localhost:8780/cockpit"
python hummingbot_api_server.py --port 8780
pause
