@echo off
TITLE n8n Supreme Mission Control Cockpit
SETLOCAL EnableDelayedExpansion

echo ========================================================
echo   n8n AUTONOMOUS MISSION CONTROL COCKPIT
echo   OMEGA Workflow Platform & LangChain Agent Engine
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/3] Checking n8n Python SDK and CLI environment...
python -c "import n8n_orchestrator; print('[OK] n8n SDK & DAG Engine loaded successfully.')" 2>NUL
IF %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Python environment not detected or missing dependencies.
)

echo.
echo [2/3] Launching n8n Mission Control Cockpit in default browser...
start "" "n8n_control_cockpit.html"

echo.
echo [3/3] Inspecting platform telemetry...
python n8n_cli.py info

echo.
echo ========================================================
echo   Mission Control Cockpit is active.
echo   To launch local REST API bridge on port 8771, run:
echo   python n8n_api_server.py
echo ========================================================
echo.
pause
