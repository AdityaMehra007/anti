@echo off
chcp 65001 >nul
title ANTIGRAVITY OMEGA - EVER GAUZY ENTERPRISE CONTROL
cd /d "e:\anti"

echo ===============================================================================
echo        ANTIGRAVITY OMEGA - EVER GAUZY ENTERPRISE ERP / CRM / ATS
echo          Candidate Ground Truth: Aditya Mehra (BBA IB DSU '26)
echo ===============================================================================
echo.
echo   [1] CHECK GAUZY HEADLESS API STATUS (REST / GraphQL)
echo   [2] RUN DRY-RUN STAGING SYNC (Candidate + 15 ATS Jobs + 15 CRM Recruiters)
echo   [3] EXECUTE LIVE GAUZY BACKEND SYNC (Requires running Gauzy server)
echo   [4] OPEN GAUZY SWAGGER API DOCUMENTATION (Browser)
echo   [5] OPEN GAUZY ONLINE DEMO / SAAS (https://demo.gauzy.co)
echo   [6] START LOCAL DOCKER COMPOSE STACK (if external/ever-gauzy cloned)
echo.
echo   [0] EXIT
echo ===============================================================================
set /p GCHOICE="Select an option [0-6]: "

if "%GCHOICE%"=="1" goto CHECK_STATUS
if "%GCHOICE%"=="2" goto RUN_DRY_RUN
if "%GCHOICE%"=="3" goto RUN_LIVE_SYNC
if "%GCHOICE%"=="4" goto OPEN_SWAGGER
if "%GCHOICE%"=="5" goto OPEN_DEMO
if "%GCHOICE%"=="6" goto START_DOCKER
if "%GCHOICE%"=="0" goto EXIT
goto EXIT

:CHECK_STATUS
cls
echo [INFO] Testing Gauzy API Connectivity...
python omega/integrations/gauzy_connector.py --status
echo.
pause
exit /b 0

:RUN_DRY_RUN
cls
echo [INFO] Executing Dry-Run Staging Synchronization...
python omega/integrations/gauzy_connector.py --dry-run --sync-all
echo.
pause
exit /b 0

:RUN_LIVE_SYNC
cls
echo [INFO] Executing Live Synchronization against Gauzy backend...
python omega/integrations/gauzy_connector.py --sync-all
echo.
pause
exit /b 0

:OPEN_SWAGGER
cls
echo [INFO] Opening Gauzy API Documentation...
start https://api.gauzy.co/docs
exit /b 0

:OPEN_DEMO
cls
echo [INFO] Opening Gauzy Interactive Demo...
start https://demo.gauzy.co
exit /b 0

:START_DOCKER
cls
echo [INFO] Checking Docker Compose Stack...
if exist "external\ever-gauzy\docker-compose.yml" (
    cd external\ever-gauzy
    docker compose -f docker-compose.infra.yml -f docker-compose.yml up -d
    cd ..\..
) else (
    echo [NOTICE] external\ever-gauzy not found. Clone via:
    echo git clone --depth 1 https://github.com/ever-co/ever-gauzy.git external/ever-gauzy
)
echo.
pause
exit /b 0

:EXIT
exit /b 0
