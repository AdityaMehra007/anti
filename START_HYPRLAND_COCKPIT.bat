@echo off
title Hyprland Autonomous Mission Control Cockpit Bridge
color 0b
echo ===============================================================================
echo   STARTING HYPRLAND AUTONOMOUS API BRIDGE & MISSION CONTROL COCKPIT
echo   Platform: hyprwm/Hyprland (Aquamarine C++23 Compositor & IPC Engine)
echo ===============================================================================
echo.
echo Starting Local REST Bridge on port 8785...
start "" "http://localhost:8785/cockpit"
python hyprland_api_server.py --port 8785
pause
