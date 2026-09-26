@echo off
setlocal enabledelayedexpansion
title Hermes Agent - Autonomous Control Center

set "HERMES_PYTHON=e:\anti\external\hermes-agent\.venv\Scripts\python.exe"
set "PYTHONIOENCODING=utf-8"

echo ===============================================================================
echo            HERMES AGENT — TAKING FULL AUTONOMOUS CONTROL
echo ===============================================================================
echo [1/3] Launching 24/7 Background Autonomous Supervisor...
start "Hermes Autonomous Controller" /min "%HERMES_PYTHON%" "e:\anti\HERMES_AUTONOMOUS_CONTROLLER.py"

echo [2/3] Opening Web Dashboard at http://127.0.0.1:9119...
timeout /t 3 /nobreak >nul
start http://127.0.0.1:9119

echo [3/3] Opening Interactive Hermes Chat REPL on your desktop...
start "Hermes Agent - Interactive Terminal" cmd /k "e:\anti\RUN_HERMES.bat"

echo ===============================================================================
echo  [SUCCESS] All Hermes Agent subsystems are now under autonomous control!
echo  - Supervisor PID and health are logged to: e:\anti\.scratch\hermes_controller_status.json
echo  - Web Dashboard: http://127.0.0.1:9119
echo  - Interactive Chat: Active in the new Command Prompt window
echo ===============================================================================
echo.
pause
