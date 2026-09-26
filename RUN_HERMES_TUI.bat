@echo off
title Hermes Agent TUI - Terminal Dashboard
color 0B
echo ===============================================================================
echo                 HERMES AGENT MODERN TUI INTERFACE
echo ===============================================================================
set PYTHONIOENCODING=utf-8
set "HERMES_PYTHON=e:\anti\external\hermes-agent\.venv\Scripts\python.exe"

if not exist "%HERMES_PYTHON%" (
    echo [ERROR] Hermes Python virtual environment not found at:
    echo         %HERMES_PYTHON%
    pause
    exit /b 1
)

"%HERMES_PYTHON%" -m hermes_cli.main --tui %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [NOTICE] Process ended with code %ERRORLEVEL%.
    pause
)
