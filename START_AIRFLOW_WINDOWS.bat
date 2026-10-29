@echo off
title OMEGA Apache Airflow Autonomous Orchestrator & Cockpit
color 0b
echo ======================================================================
echo    OMEGA APACHE AIRFLOW AUTONOMOUS ORCHESTRATION & COCKPIT LAUNCHER
echo ======================================================================
echo.

cd /d "%~dp0"

echo [*] Validating Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo [*] Launching Airflow Autonomous API Server and Cockpit on port 8775...
start "" "http://localhost:8775/cockpit"
python airflow_api_server.py --port 8775

pause
