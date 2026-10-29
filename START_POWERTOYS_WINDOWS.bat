@echo off
title Microsoft PowerToys Sovereign Autonomous Suite Launcher
color 0b
echo ===============================================================================
echo   MICROSOFT POWERTOYS SOVEREIGN AUTONOMOUS SUITE (github.com/microsoft/PowerToys)
echo ===============================================================================
echo.
echo Executing 12-Phase Sovereign Lifecycle & Attestation...
python powertoys_cli.py do-everything
echo.
echo Launching Interactive Mission Control Cockpit...
start "" "powertoys_control_cockpit.html"
echo.
pause
