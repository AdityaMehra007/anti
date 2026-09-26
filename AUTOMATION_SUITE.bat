@echo off
chcp 65001 >nul
title ANTIGRAVITY APEX AUTONOMOUS MISSION CONTROL
setlocal enabledelayedexpansion

set "ROOT_DIR=e:\anti"
set "PYTHON_EXE=%ROOT_DIR%\external\hermes-agent\.venv\Scripts\python.exe"
set "APEX_HUD=%ROOT_DIR%\apps\job_application_studio\apex_hud.html"
set "MEGA_STUDIO=%ROOT_DIR%\apps\job_application_studio\mega_studio.html"
set "STRIKE_STUDIO=%ROOT_DIR%\apps\job_application_studio\strike_300.html"
set "STUDIO_INDEX=%ROOT_DIR%\apps\job_application_studio\index.html"
set "EML_DIR=%ROOT_DIR%\applications_generated\eml_outbox"

:MENU
cls
echo ===============================================================================
echo        ANTIGRAVITY APEX AUTONOMOUS MISSION CONTROL & CAREER ENGINE
echo               Sovereign AI Operations & Bangalore Attack Vector
echo ===============================================================================
echo.
echo   [1] LAUNCH APEX MISSION CONTROL HUD (Browser)
echo       - Unified Command Center: 4,500 Employers + 300 Strike Leads + Kanban
echo       - Real-time telemetry, 1-click InMail & live pipeline state tracking
echo.
echo   [2] RUN FULL AUTONOMOUS APEX PIPELINE (Re-compile & Benchmark)
echo       - Ingests & certifies all repository data across all engines (<5s)
echo       - Commits cryptographic hashes to SQLite & refreshes all dossiers
echo.
echo   [3] OPEN BANGALORE MEGA-APPLY STUDIO (4,500+ Companies)
echo       - Direct HR Work Email dispatch (mailto:) across all Bangalore tech parks
echo.
echo   [4] OPEN 300 TARGET JOB STRIKE STUDIO (Recruiters & Decision Leads)
echo       - 96 Recruiters, 13 Hiring Managers, 92 Strategic Leads, 99 Employees
echo.
echo   [5] OPEN 15 ENTERPRISE APPLICATION DOSSIERS STUDIO
echo       - Tailored resumes, custom cover letters & STAR interview answers
echo.
echo   [6] GENERATE / OPEN BATCH RFC-822 .EML EMAIL OUTBOX
echo       - Generates ready-to-send .eml drafts and opens eml_outbox folder
echo.
echo   [7] OPEN HERMES WEB CONTROL CENTER (http://127.0.0.1:9119)
echo       - 24/7 Agent dashboard, task monitoring & skills inspector
echo.
echo   [8] LAUNCH HERMES AGENT TERMINAL TUI
echo       - Rich interactive terminal UI with 3,600+ skills & tools
echo.
echo   [9] CHECK 24/7 DAEMON & SUPERVISOR STATUS
echo       - Inspect telemetry heartbeat, active cron jobs & system uptime
echo.
echo   [10] OMNIROUTE AI GATEWAY CONTROL (Port 20128)
echo       - 352+ Providers, 150+ Free Tiers, Zero-Config Multi-Model Router
echo.
echo   [0] EXIT
echo.
echo ===============================================================================
set /p CHOICE="Select an option [0-10]: "

if "%CHOICE%"=="1" goto OPEN_APEX_HUD
if "%CHOICE%"=="2" goto RUN_APEX_PIPELINE
if "%CHOICE%"=="3" goto OPEN_MEGA_STUDIO
if "%CHOICE%"=="4" goto OPEN_STRIKE_STUDIO
if "%CHOICE%"=="5" goto OPEN_APP_STUDIO
if "%CHOICE%"=="6" goto EXPORT_EML
if "%CHOICE%"=="7" goto OPEN_DASHBOARD
if "%CHOICE%"=="8" goto LAUNCH_TUI
if "%CHOICE%"=="9" goto CHECK_STATUS
if "%CHOICE%"=="10" goto OPEN_OMNIROUTE
if "%CHOICE%"=="0" goto EXIT
goto MENU

:OPEN_APEX_HUD
echo [INFO] Launching Antigravity Apex Mission Control HUD in your browser...
start "" "%APEX_HUD%"
goto MENU

:RUN_APEX_PIPELINE
cls
echo [INFO] Running Full Autonomous Apex Pipeline Benchmark...
echo.
"%PYTHON_EXE%" "%ROOT_DIR%\omega\core\apex_orchestrator.py" --benchmark
echo.
pause
goto MENU

:OPEN_MEGA_STUDIO
echo [INFO] Opening Bangalore Mega-Apply Studio (4,500 Companies)...
start "" "%MEGA_STUDIO%"
goto MENU

:OPEN_STRIKE_STUDIO
echo [INFO] Opening 300 Target Job Strike Studio...
start "" "%STRIKE_STUDIO%"
goto MENU

:OPEN_APP_STUDIO
echo [INFO] Opening 15 Enterprise Application Dossiers Studio...
start "" "%STUDIO_INDEX%"
goto MENU

:EXPORT_EML
cls
echo [INFO] Generating batch RFC-822 .eml email drafts...
echo.
"%PYTHON_EXE%" "%ROOT_DIR%\omega\core\mega_dispatcher.py"
echo.
echo Opening eml_outbox folder...
explorer.exe "%EML_DIR%"
pause
goto MENU

:OPEN_DASHBOARD
echo [INFO] Opening Hermes Web Control Center (http://127.0.0.1:9119)...
start "" "http://127.0.0.1:9119"
goto MENU

:LAUNCH_TUI
echo [INFO] Launching Hermes Agent Terminal TUI...
start cmd.exe /k "cd /d "%ROOT_DIR%" && "%ROOT_DIR%\RUN_HERMES_TUI.bat""
goto MENU

:CHECK_STATUS
cls
echo ===============================================================================
echo                      24/7 SYSTEM TELEMETRY STATUS
echo ===============================================================================
echo.
if exist "%ROOT_DIR%\.scratch\apex_system_telemetry.json" (
    echo --- Apex Master System Telemetry ---
    type "%ROOT_DIR%\.scratch\apex_system_telemetry.json"
    echo.
)
if exist "%ROOT_DIR%\.scratch\hermes_controller_status.json" (
    echo --- Hermes Autonomous Controller Heartbeat ---
    type "%ROOT_DIR%\.scratch\hermes_controller_status.json"
    echo.
)
echo.
pause
goto MENU

:OPEN_OMNIROUTE
call "%ROOT_DIR%\START_OMNIROUTE.bat"
goto MENU

:EXIT
echo Exiting Mission Control. Background daemons remain active.
timeout /t 2 >nul
exit /b 0
