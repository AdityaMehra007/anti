@echo off
title NSA Ghidra Sovereign Autonomous SRE Suite Launcher
color 0a
echo ===============================================================================
echo   NSA GHIDRA SOVEREIGN AUTONOMOUS SUITE (github.com/NationalSecurityAgency/ghidra)
echo ===============================================================================
echo.
echo Executing 12-Phase Sovereign Lifecycle & SRE Attestation...
python ghidra_cli.py do-everything
echo.
echo Launching Interactive Mission Control Cockpit...
start "" "ghidra_control_cockpit.html"
echo.
pause
