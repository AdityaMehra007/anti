@echo off
title PowerShell Sovereign Autonomous Suite Launcher
color 0b
echo ===============================================================================
echo   POWERSHELL SOVEREIGN AUTONOMOUS SUITE (github.com/PowerShell/PowerShell)
echo ===============================================================================
echo.
echo Executing 12-Phase Sovereign Lifecycle & Attestation...
python powershell_cli.py do-everything
echo.
echo Launching Interactive Mission Control Cockpit...
start "" "powershell_control_cockpit.html"
echo.
pause
