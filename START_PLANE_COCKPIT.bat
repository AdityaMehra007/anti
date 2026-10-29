@echo off
title Plane Autonomous Mission Control Cockpit Bridge
color 0b
echo ===============================================================================
echo   STARTING PLANE AUTONOMOUS API BRIDGE & MISSION CONTROL COCKPIT
echo   Platform: makeplane/plane (CE & Cloud REST API v1)
echo ===============================================================================
echo.
echo Starting Local REST Bridge on port 8774...
start "" "http://localhost:8774/cockpit"
python plane_api_server.py --port 8774
pause
