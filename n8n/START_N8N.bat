@echo off
setlocal enabledelayedexpansion
title OMEGA :: n8n Workflow Automation Platform

echo ===============================================================================
echo                OMEGA AUTOMATION PLATFORM :: n8n ORCHESTRATOR
echo ===============================================================================
echo.

set N8N_DIR=%~dp0
cd /d "%N8N_DIR%"

if exist ".env" (
    echo [*] Loading environment from .env...
) else (
    echo [*] Initializing .env from template...
    copy ".env.example" ".env" >nul 2>&1
)

echo [*] Checking Docker daemon status...
docker info >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [*] Docker daemon is ACTIVE. Launching n8n container via Docker Compose...
    docker compose up -d
    if %ERRORLEVEL% equ 0 (
        echo [OK] n8n is running in Docker container 'omega_n8n'.
        echo [*] Access n8n at: http://localhost:5678
        start http://localhost:5678
        goto :end
    ) else (
        echo [!] Docker compose launch failed. Falling back to native npx...
    )
) else (
    echo [*] Docker daemon is not active. Using native Node.js / npx launcher...
)

echo [*] Checking for OMEGA Local Automation Engine...
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    if exist "n8n_server.py" (
        echo [OK] Launching OMEGA Automation Server on port 5678...
        start "" http://localhost:5678
        python n8n_server.py
        goto :end
    )
)

echo [*] Checking for Node.js / npx...
where npx >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Neither Python, Docker, nor npx was found.
    pause
    exit /b 1
)

echo [*] Starting n8n natively on port 5678...
set N8N_PORT=5678
set N8N_EDITOR_BASE_URL=http://localhost:5678/
set WEBHOOK_URL=http://localhost:5678/

start "" http://localhost:5678
npx n8n

:end
echo.
echo ===============================================================================
echo n8n shutdown or detached.
echo ===============================================================================
pause
