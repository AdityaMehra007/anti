@echo off
TITLE Free-For-Dev Developer Cloud & Zero-Dollar Stack Cockpit Launcher
color 0b
echo ===============================================================================
echo   FREE-FOR-DEV SOVEREIGN DEVELOPER CLOUD (github.com/ripienaar/free-for-dev)
echo   OMEGA Autonomous Zero-Dollar Architecture & Quota Engine
echo ===============================================================================
echo.

cd /d "%~dp0"

echo [1/3] Attesting Catalog & Executing 12-Phase Sovereign Lifecycle...
python free_for_dev_cli.py do-everything
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Lifecycle execution failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Starting Autonomous Local REST API Server on port 8771...
start "Free-For-Dev API Server" /min python free_for_dev_api_server.py 8771

timeout /t 2 /nobreak >NUL

echo.
echo [3/3] Launching Interactive Mission Control Cockpit in default browser...
start "" "http://localhost:8771/"

echo.
echo ===============================================================================
echo   API Server running on http://localhost:8771/
echo   Cockpit launched. You can run CLI commands in another terminal.
echo ===============================================================================
echo.
pause
