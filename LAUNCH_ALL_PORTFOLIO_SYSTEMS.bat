@echo off
title APEX OMEGA PORTFOLIO & ENTERPRISE ENGINE LAUNCHER
color 0B
echo ===============================================================================
echo                APEX OMEGA ENTERPRISE PORTFOLIO LAUNCHER
echo ===============================================================================
echo [1/3] Running Unified Automated Quality Gateway (54 Tests)...
python VERIFY_ALL_PROJECT_TESTS.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Verification failed! Aborting launch.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Opening Interactive Portfolio Showcase Portal in your browser...
start "" "portfolio_showcase\index.html"

echo.
echo [3/3] Opening ApexFlow Mission Control Cockpit...
start "" "projects\apex_enterprise_orchestrator\dashboard\index.html"

echo.
echo ===============================================================================
echo [LAUNCH COMPLETE] All systems verified 100%% green and operational.
echo You can also start the live FastAPI REST API by running:
echo   python -m uvicorn projects.apex_enterprise_orchestrator.api.server:app --port 8000
echo ===============================================================================
pause
