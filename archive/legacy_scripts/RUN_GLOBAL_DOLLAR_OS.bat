@echo off
TITLE GLOBAL DOLLAR ECONOMY OS - COMMAND CENTER
COLOR 0A

:: ============================================================================
:: GLOBAL DOLLAR ECONOMY OS -- 24/7 WINDOWS LAUNCHER & WEB APPLICATION
:: Founder: Adi | Base: Bangalore, India
:: ============================================================================

cd /d "E:\anti"

:MENU
cls
echo ============================================================================
echo        GLOBAL DOLLAR ECONOMY OS -- 24/7 MASTER COMMAND CENTER
echo ============================================================================
echo   Founder: Adi ^| Base: Bangalore, India ^| Currency: USD ($)
echo ============================================================================
echo.
echo   [W] Launch Full-Stack INTERACTIVE WEB DASHBOARD (http://localhost:8000)
echo   [1] View Live Dollar Command Center ^& Pipeline Status
echo   [2] Launch Interactive CRM ^& Dollar OS CLI Menu
echo   [3] Launch AGENTIC AI SWARM (Autonomous Prospecting ^& Sequences)
echo   [4] Start 24/7 Background Automation Daemon Loop
echo   [5] Generate Today's Morning CEO Briefing (Markdown)
echo   [6] Generate Today's Evening CEO Briefing (Markdown)
echo   [7] Run 7 Million-Dollar Skills Stress-Test Suite
echo   [8] Run System Health Check ^& Asset Inventory
echo   [9] Open Workspace Directory in File Explorer
echo   [0] Exit
echo.
echo ============================================================================
set /p choice="Select an option [W, 0-9]: "

if /i "%choice%"=="W" goto WEBAPP
if "%choice%"=="1" goto STATUS
if "%choice%"=="2" goto CLI
if "%choice%"=="3" goto SWARM
if "%choice%"=="4" goto DAEMON
if "%choice%"=="5" goto MORNING
if "%choice%"=="6" goto EVENING
if "%choice%"=="7" goto TESTSKILLS
if "%choice%"=="8" goto HEALTH
if "%choice%"=="9" goto EXPLORE
if "%choice%"=="0" goto EXIT

echo Invalid choice. Please try again.
pause
goto MENU

:WEBAPP
cls
echo Starting Interactive Web Application Server...
start "" "http://localhost:8000"
python app.py
goto MENU

:STATUS
cls
python global_dollar_daemon.py --status
echo.
pause
goto MENU

:CLI
cls
python global_dollar_daemon.py
goto MENU

:SWARM
cls
python agentic_ai_swarm.py
goto MENU

:DAEMON
cls
echo Starting continuous 24/7 Background Monitoring Daemon...
echo Press Ctrl+C at any time to stop the daemon loop.
echo.
python autonomous_revenue_autopilot.py 100
pause
goto MENU

:MORNING
cls
python global_dollar_daemon.py --morning-brief
echo.
pause
goto MENU

:EVENING
cls
python global_dollar_daemon.py --evening-brief
echo.
pause
goto MENU

:TESTSKILLS
cls
python million_dollar_skills_suite.py
echo.
pause
goto MENU

:HEALTH
cls
python global_dollar_daemon.py --health
echo.
pause
goto MENU

:EXPLORE
explorer "E:\anti"
goto MENU

:EXIT
echo Exiting Global Dollar Economy OS.
exit /b 0
