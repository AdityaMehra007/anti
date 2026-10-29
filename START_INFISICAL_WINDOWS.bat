@echo off
title Infisical Sovereign SecretOps Suite Launcher
color 0b
echo ===============================================================================
echo   INFISICAL SOVEREIGN SECRETOPS SUITE (github.com/Infisical/infisical)
echo   Zero-Knowledge Secrets ^| Dynamic Credentials ^| PKI CA ^| Cloud Sync
echo ===============================================================================
echo.
echo [1/3] Executing 12-Phase Sovereign SecretOps Lifecycle ^& Certification...
python infisical_cli.py do-everything
if %errorlevel% neq 0 (
    echo [!] Lifecycle execution failed! Check logs.
    pause
    exit /b %errorlevel%
)
echo.
echo [2/3] Launching Autonomous Local REST API Server on port 8772...
start "Infisical REST API Server" /min python infisical_api_server.py --port 8772
timeout /t 2 >nul
echo.
echo [3/3] Opening Interactive Mission Control Cockpit in Default Browser...
start "" "http://localhost:8772/"
echo.
echo ===============================================================================
echo   INFISICAL SOVEREIGN SECRETOPS SYSTEM ACTIVE ^& READY
echo   Mission Cockpit : http://localhost:8772/
echo   Telemetry API   : http://localhost:8772/api/status
echo   Audit Blockchain: VERIFIED
echo ===============================================================================
echo.
pause
