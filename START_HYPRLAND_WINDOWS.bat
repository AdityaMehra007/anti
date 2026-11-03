@echo off
title Hyprland Autonomous Sovereign Ecosystem Launcher
color 0a
echo ===============================================================================
echo   HYPRLAND SOVEREIGN AUTONOMOUS ORCHESTRATION SUITE
echo   Repository: hyprwm/Hyprland (Aquamarine C++23 Compositor)
echo ===============================================================================
echo.
echo [1/3] Generating modular configuration files...
python hyprland_cli.py config-generate

echo [2/3] Executing 12-Phase Sovereign Lifecycle Certification...
python hyprland_cli.py do-everything

echo [3/3] Launching Mission Control Cockpit on port 8785...
start "" "http://localhost:8785/cockpit"
python hyprland_api_server.py --port 8785
pause
