@echo off
TITLE Awesome Universe Intelligence Cockpit Launcher
color 0b
echo ===============================================================================
echo   GITHUB AWESOME UNIVERSE (github.com/topics/awesome ^& sindresorhus/awesome)
echo   OMEGA Sovereign Curated Knowledge ^& Manifesto Linter Cockpit
echo ===============================================================================
echo.

cd /d "%~dp0"

echo [1/3] Attesting Universe ^& Executing 12-Phase Sovereign Lifecycle...
python awesome_orchestrator.py
if %ERRORLEVEL% NEQ 0 (
    echo [!] Orchestration execution failed. Please check Python environment.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Launching Mission Control Cockpit in default browser...
start "" "%~dp0awesome_control_cockpit.html"

echo.
echo [3/3] Starting Autonomous REST API Server on port 8782...
echo       API Health:  http://127.0.0.1:8782/api/info
echo       Cockpit:     http://127.0.0.1:8782/cockpit
echo.
echo Press Ctrl+C in this console to terminate the server.
echo ===============================================================================
python awesome_api_server.py 8782
pause
