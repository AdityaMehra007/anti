@echo off
TITLE Hiring Without Whiteboards - Mission Control Cockpit
color 0B
cls
echo ===============================================================================
echo       HIRING WITHOUT WHITEBOARDS -- OMEGA CANONICAL CAREER COCKPIT
echo   761 Companies Hiring Practical Engineers (No LeetCode / Whiteboard Trivia)
echo ===============================================================================
echo.
echo [*] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH!
    pause
    exit /b 1
)

echo [*] Starting Cockpit REST API and UI Server on http://localhost:8780...
start http://localhost:8780
python hiring_without_whiteboards_engine.py --serve 8780

pause
