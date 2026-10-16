@echo off
title OMEGA MASTER JOB & COMPANY COMMAND CENTER
cd /d %~dp0
echo ==============================================================================
echo [OMEGA] LAUNCHING CAREER & COMPANY UNIVERSE (16,553 OPPORTUNITIES, 300 RECRUITERS)
echo ==============================================================================
python master_job_universe_engine.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to compile job universe telemetry.
    pause
    exit /b %ERRORLEVEL%
)
echo [OK] Opening Master Job Universe Dashboard...
start "" "master_job_universe_dashboard.html"
pause
