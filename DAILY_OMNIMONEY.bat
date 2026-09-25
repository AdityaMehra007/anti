@echo off
chcp 65001 >nul
title OMNIMONEY OS - DAILY AUTOMATION ENGINE
echo ===============================================================================
echo                ⚡ OMNIMONEY OS: DAILY CASH FLOW SPRINT ⚡
echo ===============================================================================
echo [1/3] Running Daily Intelligence, Prospect Mining and Briefing Cycle...
python -m omnimoney.run_daily
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to run daily cycle. Check python environment.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Updating Live Dashboard Data...
python omnimoney/build_dashboard_data.py

echo.
echo [3/3] Opening Live Cockpit Command Center...
start "" "e:\anti\OMNIMONEY_LIVE_COCKPIT.html"

echo.
echo ===============================================================================
echo  Daily cycle complete! Review your battle card in the opened browser window.
echo ===============================================================================
timeout /t 5
