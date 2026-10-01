@echo off
chcp 65001 >nul
title ANTIGRAVITY OMEGA - PLANE CE ENTERPRISE CONTROL
cd /d "%~dp0"

echo ===============================================================================
echo        ANTIGRAVITY OMEGA - PLANE COMMUNITY EDITION (CE) SYSTEM
echo          Modern Open-Source Sprints, Issues, Cycles & Kanban
echo ===============================================================================
echo.
echo   [1] START LOCAL PLANE CE STACK (Docker Containers + Ingress on :8095)
echo   [2] STOP LOCAL PLANE CE STACK (docker compose down)
echo   [3] CHECK STACK & CONTAINER HEALTH (Status + API Probe)
echo   [4] VIEW CONTAINER LOGS (Live Stream)
echo   [5] OPEN PLANE WEB INTERFACE (http://localhost:8095)
echo   [6] RUN OMEGA AGENT TASK DISPATCH DRY-RUN (TASK_REGISTRY -^> Plane)
echo   [7] EXECUTE LIVE AGENT TASK SYNCHRONIZATION
echo   [8] START PLANE WEBHOOK LISTENER (Port :8096)
echo   [9] PROVISION DEPARTMENT BOARDS & SPRINTS (Core, Cap, Fleet, Intel)
echo   [D] OPEN PLANE CONTROL CENTER DASHBOARD (Browser Cockpit)
echo.
echo   [0] EXIT
echo ===============================================================================
set /p PCHOICE="Select an option [0-9, D]: "

if /i "%PCHOICE%"=="D" goto OPEN_DASHBOARD
if "%PCHOICE%"=="1" goto START_STACK
if "%PCHOICE%"=="2" goto STOP_STACK
if "%PCHOICE%"=="3" goto CHECK_STATUS
if "%PCHOICE%"=="4" goto VIEW_LOGS
if "%PCHOICE%"=="5" goto OPEN_BROWSER
if "%PCHOICE%"=="6" goto RUN_DRY_RUN
if "%PCHOICE%"=="7" goto RUN_LIVE_SYNC
if "%PCHOICE%"=="8" goto START_WEBHOOK
if "%PCHOICE%"=="9" goto PROVISION_BOARDS
if "%PCHOICE%"=="0" goto EXIT
goto EXIT

:START_STACK
cls
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0START_PLANE.ps1" -Action up
echo.
pause
exit /b 0

:STOP_STACK
cls
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0START_PLANE.ps1" -Action down
echo.
pause
exit /b 0

:CHECK_STATUS
cls
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0START_PLANE.ps1" -Action status
echo.
pause
exit /b 0

:VIEW_LOGS
cls
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0START_PLANE.ps1" -Action logs
echo.
pause
exit /b 0

:OPEN_BROWSER
cls
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0START_PLANE.ps1" -Action browser
exit /b 0

:RUN_DRY_RUN
cls
echo [INFO] Running Plane Task Dispatcher in Simulation / Dry-Run Mode...
python omega/orchestration/plane_dispatcher.py --dry-run
echo.
pause
exit /b 0

:RUN_LIVE_SYNC
cls
echo [INFO] Running Live Task Sync against Plane Instance...
python omega/orchestration/plane_dispatcher.py --sync
echo.
pause
exit /b 0

:START_WEBHOOK
cls
echo [INFO] Starting Plane Webhook Reactor on Port 8096...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0START_PLANE.ps1" -Action webhook
echo.
pause
exit /b 0

:PROVISION_BOARDS
cls
echo [INFO] Provisioning Departmental Boards & 14-Day Sprint Cycles...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0START_PLANE.ps1" -Action provision
echo.
pause
exit /b 0

:OPEN_DASHBOARD
cls
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0START_PLANE.ps1" -Action dashboard
exit /b 0

:EXIT
exit /b 0
