@echo off
title Daily Career Morning Briefing
cd /d "%~dp0"
echo [*] Generating Daily Action Briefing...
python automation\daily_career_briefing.py
echo.
echo [*] Opening DAILY_BRIEFING.md...
start "" "DAILY_BRIEFING.md"
timeout /t 3 >nul
