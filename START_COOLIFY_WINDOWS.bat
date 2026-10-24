@echo off
TITLE Coolify v4 Windows Orchestration Launcher
SETLOCAL EnableDelayedExpansion

echo ========================================================
echo   COOLIFY v4 AUTONOMOUS ENTERPRISE ORCHESTRATOR
echo   OMEGA Platform Infrastructure Suite
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python orchestrator environment...
python -c "import coolify_orchestrator; print('Coolify SDK loaded successfully.')" 2>NUL
IF %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Python environment not detected or missing dependencies.
) ELSE (
    echo [OK] Python SDK and CLI ready.
)

echo.
echo [2/3] Checking Docker Desktop status...
docker info >NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [NOTICE] Docker daemon is not active.
    echo Running Coolify in Autonomous High-Fidelity Simulation Mode.
    echo You can start Docker Desktop anytime to switch to live container execution.
) ELSE (
    echo [OK] Docker daemon is online and responsive.
)

echo.
echo [3/3] Launching Coolify Mission Control Cockpit...
start "" "coolify_control_cockpit.html"

echo.
echo Running cluster inspection...
python coolify_cli.py info

echo.
echo ========================================================
echo   Cockpit launched in browser.
echo   Press any key to test full OMEGA stack deployment...
echo ========================================================
pause >NUL

python coolify_cli.py stack
echo.
pause
