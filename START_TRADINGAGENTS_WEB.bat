@echo off
setlocal
title TradingAgents Streamlit Web Cockpit
cd /d "%~dp0projects\TradingAgents"
echo =====================================================================
echo  TradingAgents: Autonomous Web Cockpit
echo  Launching Streamlit GUI at http://localhost:8501
echo =====================================================================
echo.
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in projects\TradingAgents\.venv
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
streamlit run app.py
pause
