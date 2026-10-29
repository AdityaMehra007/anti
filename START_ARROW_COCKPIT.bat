@echo off
title Apache Arrow Mission Control Cockpit Bridge
color 0a
echo ===============================================================================
echo   STARTING APACHE ARROW AUTONOMOUS API BRIDGE & MISSION CONTROL COCKPIT
echo ===============================================================================
echo.
echo Starting Local REST Bridge on port 8775...
start "" "http://localhost:8775/cockpit"
python arrow_api_server.py --port 8775
pause
