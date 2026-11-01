@echo off
title Hummingbot Sovereign Autonomous Suite Launcher
color 0b
echo ===============================================================================
echo   HUMMINGBOT SOVEREIGN AUTONOMOUS SUITE (https://github.com/hummingbot/hummingbot)
echo ===============================================================================
echo.
echo Executing 12-Phase Sovereign Lifecycle & Attestation...
python hummingbot_cli.py do-everything
echo.
echo Launching Interactive Mission Control Cockpit...
start "" "hummingbot_control_cockpit.html"
echo.
pause
