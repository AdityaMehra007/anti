@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo     freeCodeCamp AUTONOMOUS CONTROL LAUNCHER
echo ===================================================
echo [1/2] Verifying PowerShell Execution...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0START_FREECODECAMP.ps1" %*

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] freeCodeCamp launcher encountered an issue. See details above.
    pause
)
