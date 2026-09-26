@echo off
setlocal enabledelayedexpansion
title Hermes Agent - Master Control Center

set "HERMES_PYTHON=e:\anti\external\hermes-agent\.venv\Scripts\python.exe"
set "PYTHONIOENCODING=utf-8"

:menu
cls
echo ===============================================================================
echo                     NOUS RESEARCH - HERMES AGENT CONTROL CENTER
echo ===============================================================================
echo   Workspace : e:\anti
echo   Python    : %HERMES_PYTHON%
echo   Skills    : 3,679 Active Skills Loaded
echo   Provider  : OpenRouter (nvidia/nemotron-3.5-lightning:free)
echo ===============================================================================
echo.
echo   [1] Launch Interactive Hermes Agent (Classic REPL)
echo   [2] Launch Modern Full-Screen TUI (Rich Textual UI)
echo   [3] Start Web Dashboard (Browser UI on http://127.0.0.1:9119)
echo   [4] Stop Web Dashboard Processes
echo   [5] Check Web Dashboard Status
echo   [6] Launch ACP Server (Agent Client Protocol for IDEs)
echo   [7] Check Scheduled Tasks (hermes cron list)
echo   [8] Show Agent Configuration & Model Details
echo   [9] View Hermes Memory & User Profile
echo   [S] List / Verify Mounted Skills
echo   [Q] Exit Control Center
echo.
echo ===============================================================================
set /p choice="Select an option (1-9, S, Q): "

if /i "%choice%"=="1" goto run_cli
if /i "%choice%"=="2" goto run_tui
if /i "%choice%"=="3" goto start_dashboard
if /i "%choice%"=="4" goto stop_dashboard
if /i "%choice%"=="5" goto status_dashboard
if /i "%choice%"=="6" goto run_acp
if /i "%choice%"=="7" goto run_cron
if /i "%choice%"=="8" goto run_config
if /i "%choice%"=="9" goto run_memory
if /i "%choice%"=="S" goto run_skills
if /i "%choice%"=="Q" goto end
goto menu

:run_cli
echo.
echo Starting Interactive Hermes Agent in a new window...
start "Hermes Agent - Interactive CLI" cmd /k "e:\anti\RUN_HERMES.bat"
goto menu

:run_tui
echo.
echo Starting Modern Fullscreen TUI in a new window...
start "Hermes Agent - TUI" cmd /k "e:\anti\RUN_HERMES_TUI.bat"
goto menu

:start_dashboard
echo.
echo Starting Hermes Web Dashboard on http://127.0.0.1:9119...
start "Hermes Web Dashboard" cmd /k "cd /d e:\anti\external\hermes-agent && set PYTHONIOENCODING=utf-8 && "%HERMES_PYTHON%" -m hermes_cli.main dashboard --skip-build"
echo Dashboard launched. Opening http://127.0.0.1:9119 in browser...
start http://127.0.0.1:9119
pause
goto menu

:stop_dashboard
echo.
echo Stopping all running Hermes web dashboard processes...
"%HERMES_PYTHON%" -m hermes_cli.main dashboard --stop
pause
goto menu

:status_dashboard
echo.
echo Checking Hermes web server process status...
"%HERMES_PYTHON%" -m hermes_cli.main dashboard --status
pause
goto menu

:run_acp
echo.
echo Starting Hermes ACP Server...
start "Hermes ACP Server" cmd /k "cd /d e:\anti && set PYTHONIOENCODING=utf-8 && "%HERMES_PYTHON%" -m hermes_cli.main acp"
echo ACP server started.
pause
goto menu

:run_cron
echo.
echo === Scheduled Tasks (Cron) ===
"%HERMES_PYTHON%" -m hermes_cli.main cron list
echo.
pause
goto menu

:run_config
echo.
echo === Hermes Configuration ===
"%HERMES_PYTHON%" -m hermes_cli.main config
echo.
pause
goto menu

:run_memory
echo.
echo === Hermes Memory Directory ===
type "%LOCALAPPDATA%\hermes\memories\USER.md" 2>nul || echo No USER.md profile yet.
echo.
pause
goto menu

:run_skills
echo.
echo === Hermes Skills Summary ===
"%HERMES_PYTHON%" -m hermes_cli.main skills list
echo.
pause
goto menu

:end
echo Exiting Control Center. Goodbye!
exit /b 0
