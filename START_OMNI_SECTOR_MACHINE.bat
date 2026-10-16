@echo off
title OMEGA OMNI-SECTOR WEALTH MACHINE
cd /d %~dp0
echo ==============================================================================
echo [OMEGA] EXECUTING OMNI-SECTOR WEALTH & DAILY CASH ENGINE (FULL POWERMODE)
echo ==============================================================================
python omni_sector_money_machine.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Pipeline execution encountered an issue.
    pause
    exit /b %ERRORLEVEL%
)
echo [OK] Opening Omni-Sector Wealth Dashboard...
start "" "omni_sector_wealth_dashboard.html"
pause
