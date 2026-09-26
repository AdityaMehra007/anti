@echo off
title VECTIS TRADE — Master Operating System Autopilot
cd /d %~dp0

echo =======================================================
echo VECTIS TRADE TECHNOLOGIES PRIVATE LIMITED
echo Autonomous Export Compliance & Letter of Credit Gateway
echo =======================================================
echo.

echo [1/3] Running ICC UCP 600 Compliance & End-to-End Test Suite...
pytest test_vectis_core.py test_vectis_end_to_end.py -v
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Tests failed! Aborting launch.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Mining Real Network Leads from LinkedIn Export...
python vectis_network_miner.py

echo.
echo [3/3] Launching Master Autopilot (Daemon + Agents + Web Portal)...
start http://localhost:8080
python RUN_VECTIS_AUTOPILOT.py

pause
