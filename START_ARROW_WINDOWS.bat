@echo off
title Apache Arrow Sovereign Autonomous Suite Launcher
color 0b
echo ===============================================================================
echo   APACHE ARROW SOVEREIGN AUTONOMOUS SUITE (https://github.com/apache/arrow)
echo ===============================================================================
echo.
echo Executing 12-Phase Sovereign Lifecycle & Attestation...
python arrow_cli.py do-everything
echo.
echo Launching Interactive Mission Control Cockpit...
start "" "arrow_control_cockpit.html"
echo.
pause
