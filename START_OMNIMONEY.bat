@echo off
title OMNIMONEY OS - Autonomous Command Center
color 0A
echo ========================================================
echo   OMNIMONEY OS: MONEY RADAR BENGALURU
echo   Economic Opportunity, B2B Cash Flow ^& Capital Engine
echo ========================================================
echo.

echo [1/4] Synchronizing Database ^& Opportunity Pipelines...
python -m omnimoney.build_dashboard_data
if %errorlevel% neq 0 (
    echo [ERROR] Failed to synchronize data.
    pause
    exit /b %errorlevel%
)

echo.
echo [2/4] Generating Morning CEO Briefing...
python -c "from omnimoney.omnimoney_engine import OmniMoneyEngine; from omnimoney.b2b_sales_engine import B2BSalesEngine; from omnimoney.morning_brief import MorningBriefEngine; MorningBriefEngine(OmniMoneyEngine(), B2BSalesEngine()).save_brief_report()"
echo [OK] Saved reports/DAILY_CEO_BRIEF.md

echo.
echo [3/4] Launching Interactive Money Radar Bengaluru Cockpit...
start "" "OMNIMONEY_RADAR_BENGALURU.html"

echo.
echo [4/4] Starting FastAPI Production Server on http://127.0.0.1:8000/docs ...
echo Press Ctrl+C to terminate server when finished.
echo.
uvicorn omnimoney.server:app --host 127.0.0.1 --port 8000 --reload
