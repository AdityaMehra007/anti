@echo off
title AI Career Command Center
echo ======================================================================
echo   STARTING AI CAREER COMMAND CENTER COCKPIT
echo   Candidate: Aditya Mehra | Base: Bengaluru
echo ======================================================================
echo.

cd /d "%~dp0"

echo [*] Regenerating latest pipeline telemetry...
python projects\flagship-career-engine\generate_dashboard.py

echo.
echo [*] Launching Interactive Cockpit in default browser...
start "" "projects\flagship-career-engine\index.html"

echo.
echo [OK] Command Center active. You can close this window.
timeout /t 3 >nul
