@echo off
title Plane Sovereign Autonomous Suite Launcher
color 0b
echo ===============================================================================
echo   PLANE SOVEREIGN AUTONOMOUS SUITE (github.com/makeplane/plane)
echo   Issues, Sprint Cycles, Kanban, Modules, Pages & Multi-Agent Reactor
echo ===============================================================================
echo.
echo Executing 12-Phase Sovereign Lifecycle & Attestation...
python plane_cli.py do-everything
echo.
echo Launching Interactive Mission Control Cockpit...
start "" "plane_control_cockpit.html"
echo.
pause
