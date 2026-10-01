@echo off
chcp 65001 > nul
title OMNI-SYSTEM :: Universal Sovereign Operating System
color 0A

echo ==========================================================================
echo   OMNI-SYSTEM :: UNIVERSAL AUTONOMOUS SOVEREIGN ENGINE
echo   OPERATOR: Aditya Mehra ^| Bengaluru, India
echo   DAEMONS: Port 8765 (Revenue OS) ^| Port 8766 (Global Capital OS)
echo ==========================================================================
echo.

echo [1/4] Verifying and Activating Sovereign Daemons...
start "REVENUE_OS_8765" /min cmd /c "python -m REVENUE_OS --serve --port 8765"
timeout /t 2 /nobreak > nul
start "GLOBAL_CAPITAL_8766" /min cmd /c "python -m uvicorn GLOBAL_CAPITAL_OS.web.server:app --port 8766"
timeout /t 2 /nobreak > nul

echo [2/4] Querying Unified Telemetry & Financial Ledgers...
python -m OMNI_SYSTEM --status
echo.

echo [3/4] Launching Flagship 0000 Mission Control HUD in Web Browser...
start apps\omni_command\index.html

echo.
echo ==========================================================================
echo   SOVEREIGN COMMAND MENU
echo ==========================================================================
:MENU
echo.
echo   [1] Refresh Live Status & Briefing
echo   [2] Daily Cash Hunter & Quota Audit
echo   [3] Open 1-Click B2B Email Strike Launcher
echo   [4] Open Worldwide Direct Pay Portal (Any Currency / Any Amount)
echo   [5] Run Full System Validation Suite (111 Tests)
echo   [6] Open Master Apps Index (25 Web Apps)
echo   [7] Open $110T World GDP Daily Cash Tap
echo   [8] Open Plane CE Control Center & Task Dispatch Hub
echo   [0] Exit Menu
echo.
set /p opt="Select an action [0-8]: "

if "%opt%"=="1" (
    cls
    python -m OMNI_SYSTEM --status
    goto MENU
)
if "%opt%"=="2" (
    cls
    python -m OMNI_SYSTEM --hunt
    goto MENU
)
if "%opt%"=="3" (
    start apps\daily_cash_machine\b2b_strike_launcher.html
    echo Opened B2B Strike Launcher.
    goto MENU
)
if "%opt%"=="4" (
    start apps\global_pay\index.html
    echo Opened Worldwide Direct Pay Portal.
    goto MENU
)
if "%opt%"=="5" (
    cls
    python scripts\validate_all.py
    goto MENU
)
if "%opt%"=="6" (
    start apps\index.html
    echo Opened 25-App Master Directory.
    goto MENU
)
if "%opt%"=="7" (
    start apps\world_gdp_tap\index.html
    python -m OMNI_SYSTEM --siphon
    goto MENU
)
if "%opt%"=="8" (
    cls
    start "" "PLANE_CONTROL_CENTER.html"
    python -m terra_kinetics.cli --plane-status
    pause
    goto MENU
)
if "%opt%"=="0" (
    echo Exiting OMNI-SYSTEM Console. Daemons remain active in background.
    exit /b 0
)

echo Invalid selection. Please choose 0 to 8.
goto MENU
