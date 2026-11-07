@echo off
title CAREER-OPS SOVEREIGN MISSION CONTROL & ORCHESTRATOR
color 0A
cls
echo ===============================================================================
echo        CAREER-OPS SOVEREIGN MISSION CONTROL & REST ENGINE (v1.39.0)
echo ===============================================================================
echo.
echo [1/3] Verifying CareerOps Sovereign Environment...
if not exist "e:\anti\career-ops" (
    echo [ERROR] career-ops directory not found at e:\anti\career-ops!
    pause
    exit /b 1
)

echo [2/3] Launching CareerOps REST Server on http://127.0.0.1:8794 ...
start /B "CareerOps Engine" python e:\anti\career_ops_orchestrator.py --serve --port 8794

timeout /t 2 /nobreak >nul

echo [3/3] Opening CareerOps Mission Control Cockpit in default browser...
start http://127.0.0.1:8794/cockpit

echo.
echo ===============================================================================
echo  CAREER-OPS SOVEREIGN ENGINE ACTIVE:
echo  - Mission Control Cockpit: http://127.0.0.1:8794/cockpit
echo  - REST API Telemetry:     http://127.0.0.1:8794/api/stats
echo  - Press Ctrl+C in this console or close the window to terminate the server.
echo ===============================================================================
pause
