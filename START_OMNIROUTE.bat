@echo off
chcp 65001 >nul
title OMNIROUTE AI GATEWAY COMMAND CENTER
setlocal enabledelayedexpansion

set "ROOT_DIR=e:\anti"
set "PORT=20128"
set "GATEWAY_URL=http://localhost:!PORT!"
set "PATH=E:\anti gravity\npm-global;%PATH%"

if not "%~1"=="" (
    if /i "%~1"=="start" goto START_GATEWAY_SILENT
    if /i "%~1"=="status" goto CHECK_STATUS_CLI
    if /i "%~1"=="stop" goto STOP_GATEWAY_CLI
    if /i "%~1"=="test" goto RUN_TEST_CLI
    if /i "%~1"=="dashboard" goto OPEN_DASHBOARD_CLI
)

:MENU
cls
echo ===============================================================================
echo            OMNIROUTE UNIFIED AI GATEWAY - SOVEREIGN CONTROLLER
echo            Port: !PORT!  ^|  352+ Providers  ^|  150+ Free Tiers  ^|  RTK/Caveman
echo ===============================================================================
echo.
powershell -NoProfile -Command "try { $c = Get-NetTCPConnection -LocalPort !PORT! -ErrorAction Stop; Write-Host ' [STATUS] GATEWAY IS ACTIVE (Listening on port !PORT!)' -ForegroundColor Green } catch { Write-Host ' [STATUS] GATEWAY IS OFFLINE (Port !PORT! inactive)' -ForegroundColor Yellow }"
echo.
echo   [1] START OMNIROUTE GATEWAY (Background / Dedicated Window)
echo       - Launches unified OpenAI/Anthropic proxy on !GATEWAY_URL!/v1
echo.
echo   [2] OPEN WEB DASHBOARD & FREE TIERS POOL
echo       - Visual inspection: !GATEWAY_URL!/dashboard/free-tiers
echo.
echo   [3] RUN GATEWAY DIAGNOSTICS & DOCTOR
echo       - Checks local credentials, catalog, network, and providers
echo.
echo   [4] SEND TEST PROMPT TO ZERO-CONFIG 'AUTO' MODEL
echo       - Verifies live fallback chain and token response
echo.
echo   [5] STOP / TERMINATE RUNNING GATEWAY
echo       - Gracefully releases port !PORT!
echo.
echo   [6] RUN OMEGA HARDENED COMPLIANCE SUITE (18 Tests)
echo       - Strict verified evaluation of latency, fallback, cache & security
echo.
echo   [7] OPEN AGENT INTEGRATION GUIDE (OpenCode, Claude, Cursor, Cline)
echo.
echo   [0] EXIT
echo.
echo ===============================================================================
set /p CHOICE="Select an option [0-7]: "

if "%CHOICE%"=="1" goto START_GATEWAY
if "%CHOICE%"=="2" goto OPEN_DASHBOARD
if "%CHOICE%"=="3" goto RUN_DOCTOR
if "%CHOICE%"=="4" goto RUN_TEST
if "%CHOICE%"=="5" goto STOP_GATEWAY
if "%CHOICE%"=="6" goto RUN_TEST_SUITE
if "%CHOICE%"=="7" goto OPEN_GUIDE
if "%CHOICE%"=="0" goto EXIT
goto MENU

:START_GATEWAY
echo.
echo [INFO] Checking if OmniRoute is already listening on port !PORT!...
powershell -NoProfile -Command "$c = Get-NetTCPConnection -LocalPort !PORT! -ErrorAction SilentlyContinue; if ($c) { Write-Host '[OK] OmniRoute is ALREADY running on port !PORT!.' -ForegroundColor Green; exit 0 } else { exit 1 }"
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Gateway already running.
    timeout /t 2 >nul
    goto MENU
)

echo [INFO] Spawning OmniRoute Gateway daemon...
start "OmniRoute Gateway Daemon (Port !PORT!)" cmd /k "title OmniRoute Gateway Daemon && chcp 65001 >nul && omniroute serve --no-open"
echo [INFO] Waiting for port !PORT! to open...
powershell -NoProfile -Command "$running = $false; for ($i=0; $i -lt 15; $i++) { Start-Sleep -Seconds 1; if (Get-NetTCPConnection -LocalPort !PORT! -ErrorAction SilentlyContinue) { $running = $true; break } }; if ($running) { Write-Host '[OK] Gateway successfully bound to !GATEWAY_URL!' -ForegroundColor Green } else { Write-Host '[WARN] Gateway is taking longer to initialize or running in background.' -ForegroundColor Yellow }"
pause
goto MENU

:START_GATEWAY_SILENT
start "OmniRoute Gateway Daemon (Port !PORT!)" cmd /k "title OmniRoute Gateway Daemon && chcp 65001 >nul && omniroute serve --no-open"
exit /b 0

:OPEN_DASHBOARD
echo [INFO] Opening OmniRoute Web Dashboard...
start "" "!GATEWAY_URL!"
goto MENU

:OPEN_DASHBOARD_CLI
start "" "!GATEWAY_URL!"
exit /b 0

:RUN_DOCTOR
cls
echo ===============================================================================
echo                      RUNNING OMNIROUTE DOCTOR DIAGNOSTICS
echo ===============================================================================
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%ROOT_DIR%\scripts\run_omniroute.ps1" status
echo.
pause
goto MENU

:CHECK_STATUS_CLI
powershell -NoProfile -ExecutionPolicy Bypass -File "%ROOT_DIR%\scripts\run_omniroute.ps1" status
exit /b 0

:RUN_TEST
cls
echo ===============================================================================
echo                     TESTING ZERO-CONFIG 'AUTO' ROUTING
echo ===============================================================================
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%ROOT_DIR%\scripts\run_omniroute.ps1" test "Verify gateway operational from Antigravity Command Center"
echo.
pause
goto MENU

:RUN_TEST_CLI
powershell -NoProfile -ExecutionPolicy Bypass -File "%ROOT_DIR%\scripts\run_omniroute.ps1" test "%~2"
exit /b 0

:STOP_GATEWAY
cls
echo [INFO] Terminating processes bound to port !PORT!...
powershell -NoProfile -Command "$conns = Get-NetTCPConnection -LocalPort !PORT! -ErrorAction SilentlyContinue; if ($conns) { $pids = $conns.OwningProcess | Select-Object -Unique; foreach ($p in $pids) { Write-Host \"Killing process PID: $p\"; Stop-Process -Id $p -Force }; Write-Host '[OK] Gateway terminated.' -ForegroundColor Green } else { Write-Host '[INFO] No process found on port !PORT!.' -ForegroundColor Cyan }"
pause
goto MENU

:STOP_GATEWAY_CLI
powershell -NoProfile -Command "$conns = Get-NetTCPConnection -LocalPort !PORT! -ErrorAction SilentlyContinue; if ($conns) { $pids = $conns.OwningProcess | Select-Object -Unique; foreach ($p in $pids) { Stop-Process -Id $p -Force } }"
exit /b 0

:RUN_TEST_SUITE
cls
echo ===============================================================================
echo               RUNNING OMEGA OMNIROUTE HARDENED TEST SUITE (18 TESTS)
echo ===============================================================================
echo.
python "%ROOT_DIR%\tests\test_omniroute_live.py"
echo.
pause
goto MENU

:OPEN_GUIDE
start "" "%ROOT_DIR%\docs\ai\OMNIROUTE_AGENT_INTEGRATION.md"
goto MENU

:EXIT
exit /b 0
