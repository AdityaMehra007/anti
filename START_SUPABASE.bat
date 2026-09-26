@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo       SUPABASE AUTONOMOUS CONTROL LAUNCHER
echo ===================================================
echo [1/3] Verifying PowerShell Execution...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0START_SUPABASE.ps1"

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Supabase launcher encountered an issue. See details above.
    pause
)
