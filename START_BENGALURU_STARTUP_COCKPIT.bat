@echo off
title Bengaluru Startup Intelligence Cockpit - Port 8792
color 0b

echo ===============================================================================
echo            BENGALURU STARTUP INTELLIGENCE MISSION CONTROL (BSIE-X)
echo                Curated for: Adi (BBA International Business)
echo ===============================================================================
echo.
echo [1/3] Initializing and seeding relational SQLite database...
python "%~dp0bengaluru_startup_intel_engine.py" --export

echo.
echo [2/3] Launching local REST API server on http://127.0.0.1:8792 ...
start "BSIE-X API Server" /B python "%~dp0bengaluru_startup_intel_engine.py" --serve 8792

echo.
echo [3/3] Launching Interactive Cockpit in default browser...
timeout /t 2 /nobreak >nul
start http://127.0.0.1:8792/cockpit

echo.
echo ===============================================================================
echo  Cockpit is LIVE at http://127.0.0.1:8792/cockpit
echo  Application dossiers available in e:\anti\applications_generated\bengaluru_intel\
echo ===============================================================================
pause
