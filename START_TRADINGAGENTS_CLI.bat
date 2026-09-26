@echo off
setlocal
title TradingAgents Interactive CLI Cockpit
cd /d "%~dp0projects\TradingAgents"
echo =====================================================================
echo  TradingAgents: Multi-Agent LLM Financial Trading Framework
echo  Autonomous Multi-Agent LangGraph System
echo =====================================================================
echo.
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in projects\TradingAgents\.venv
    echo Please ensure dependencies are installed.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
python -m cli.main
pause
