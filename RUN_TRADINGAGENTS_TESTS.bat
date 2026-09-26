@echo off
setlocal
title TradingAgents Automated Test Runner
cd /d "%~dp0projects\TradingAgents"
echo =====================================================================
echo  TradingAgents Test Runner (Pytest Verification Gate)
echo =====================================================================
echo.
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in projects\TradingAgents\.venv
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
pytest tests/test_omni_integration.py -v
pause
