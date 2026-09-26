@echo off
title Hermes Agent Command Center (Nous Research)
color 0A
echo ===============================================================================
echo               HERMES AGENT - AUTONOMOUS AI AGENT LAUNCHER
echo ===============================================================================
echo [INFO] Workspace: E:\anti
echo [INFO] Provider: OpenRouter (Active)
echo [INFO] Skills Loaded: 3,679 (51 Nous Bundled + 3,628 Workspace Skills)
echo [INFO] Capabilities: Delegation, Memory (FTS5 WAL), Tools, Gateway, TUI
echo ===============================================================================

set PYTHONIOENCODING=utf-8
set "HERMES_PYTHON=e:\anti\external\hermes-agent\.venv\Scripts\python.exe"

if not exist "%HERMES_PYTHON%" (
    echo [ERROR] Hermes Python virtual environment not found at:
    echo         %HERMES_PYTHON%
    pause
    exit /b 1
)

if "%~1"=="" (
    echo [INFO] Launching interactive session...
    echo.
    "%HERMES_PYTHON%" -m hermes_cli.main
) else (
    "%HERMES_PYTHON%" -m hermes_cli.main %*
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [NOTICE] Process ended with code %ERRORLEVEL%.
    pause
)
