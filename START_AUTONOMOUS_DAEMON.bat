@echo off
title OMEGA AUTONOMOUS DAILY ECOSYSTEM DAEMON
cd /d "e:\anti"
echo ==============================================================================
echo   ANTIGRAVITY OMEGA: 24/7 AUTONOMOUS DAILY ECOSYSTEM DAEMON
echo   Interval: 24.0 Hours | Mode: Perpetual Autonomous Execution
echo ==============================================================================
:loop
echo [%date% %time%] Launching Autonomous Daily Ecosystem cycle...
"C:\Users\amehr\AppData\Local\Programs\Python\Python313\python.exe" "e:\anti\AUTONOMOUS_DAILY_ECOSYSTEM.py" --once
if %errorlevel% neq 0 (
    echo [!] Warning: Cycle finished with exit code %errorlevel%. Pausing 60s before retry...
    timeout /t 60 /nobreak >nul
) else (
    echo [*] Cycle completed successfully. Sleeping for 24 hours (86,400 seconds)...
    timeout /t 86400 /nobreak >nul
)
goto loop
