@echo off
title FORTUNE 500 SOVEREIGN DAEMON (OMEGA INF)
echo ================================================================================
echo           FORTUNE 500 SOVEREIGN ENTERPRISE DAEMON & REST API SERVER
echo ================================================================================
echo [!] Verifying Environment & Running Pytest Gateways...
python -m pytest fortune_500_projects/test_fortune500_all_sectors.py tests/test_fortune500_ecosystem.py -q
if %ERRORLEVEL% NEQ 0 (
    echo [X] Tests failed. Aborting startup.
    pause
    exit /b %ERRORLEVEL%
)
echo [+] All 12 Quality Gateways Verified Green (100%%).
echo.
echo [!] Launching Cockpit UI in default browser...
start http://127.0.0.1:8888/cockpit
echo [!] Starting High-Concurrency REST API Server on port 8888...
echo     - Endpoint: http://127.0.0.1:8888/api/projects
echo     - Telemetry: http://127.0.0.1:8888/api/telemetry
echo     - Press Ctrl+C to terminate the daemon.
echo.
python fortune_500_server.py 8888
pause
