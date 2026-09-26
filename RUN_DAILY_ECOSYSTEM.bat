@echo off
chcp 65001 >nul
title ADI CAREER OS - AUTONOMOUS DAILY ECOSYSTEM MASTER
cd /d "e:\anti"

echo ===============================================================================
echo        ADI CAREER OS - AUTONOMOUS DAILY ECOSYSTEM & 24/7 DAEMON
echo            Candidate: Aditya Mehra (BBA International Business '26)
echo ===============================================================================
echo.
echo   [1] RUN COMPLETE DAILY CAREER CYCLE (Single Immediate Execution)
echo       - Full database & workspace audit
echo       - ADI CAREER OS: 10-Factor Scorer, Sales Filter, Approval Clearance
echo       - RUN_AUTONOMOUS_PIPELINE.py: 51 Dossiers, 300 Strike, 4,500 Employers
echo       - Portfolio Engines & Automated Test Certification
echo.
echo   [2] START PERSISTENT 24/7 AUTONOMOUS DAILY DAEMON (Runs every 24 Hours)
echo       - Keeps console active, runs cycle at set interval
echo.
echo   [3] LAUNCH JOB APPLICATION STUDIO COMMAND CENTER (Browser)
echo.
echo   [4] OPEN HERMES WEB CONTROL DASHBOARD (http://127.0.0.1:9119)
echo.
echo   [0] EXIT
echo.
echo ===============================================================================
set /p CHOICE="Select an option [0-4]: "

if "%CHOICE%"=="1" goto RUN_ONCE
if "%CHOICE%"=="2" goto RUN_DAEMON
if "%CHOICE%"=="3" goto OPEN_STUDIO
if "%CHOICE%"=="4" goto OPEN_DASHBOARD
if "%CHOICE%"=="0" goto EXIT
goto EXIT

:RUN_ONCE
cls
echo [INFO] Running Complete Daily Autonomous Career Cycle...
python AUTONOMOUS_DAILY_ECOSYSTEM.py --once
echo.
pause
exit /b 0

:RUN_DAEMON
cls
echo [INFO] Starting Persistent Autonomous 24/7 Daemon...
python AUTONOMOUS_DAILY_ECOSYSTEM.py --daemon --interval 24.0
pause
exit /b 0

:OPEN_STUDIO
start "" "apps\job_application_studio\command_center.html"
exit /b 0

:OPEN_DASHBOARD
start "" "http://127.0.0.1:9119"
exit /b 0

:EXIT
exit /b 0
