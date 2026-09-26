@echo off
title OMEGA ∞ — Autonomous AI Operating System
cls
echo ===============================================================================
echo                OMEGA INFINITY: AUTONOMOUS AI OPERATING SYSTEM
echo                 Master Constitution: OMEGA_CONSTITUTION.md
echo ===============================================================================
echo.
echo Select Execution Command:
echo   [1] OMEGA (Full System Status ^& Verification)
echo   [2] FULL POWER (Activate All 9 Executive Departments)
echo   [3] DO EVERYTHING (Prioritize ^& Execute Safe Workflows)
echo   [4] AUDIT (Adversarial Weakness ^& Bottleneck Scan)
echo   [5] RED TEAM (12 Core Probes Stress Test)
echo   [6] LAUNCH COMMAND COCKPIT (Open Interactive Dark-Mode UI)
echo   [7] EXIT
echo.
set /p opt="Enter selection [1-7]: "

if "%opt%"=="1" (
    python omega\core\omega_infinity_runtime.py --command "OMEGA"
    pause
    goto :eof
)
if "%opt%"=="2" (
    python omega\core\omega_infinity_runtime.py --command "FULL POWER"
    pause
    goto :eof
)
if "%opt%"=="3" (
    python omega\core\omega_infinity_runtime.py --command "DO EVERYTHING"
    pause
    goto :eof
)
if "%opt%"=="4" (
    python omega\core\omega_infinity_runtime.py --command "AUDIT"
    pause
    goto :eof
)
if "%opt%"=="5" (
    python omega\core\omega_infinity_runtime.py --command "RED TEAM"
    pause
    goto :eof
)
if "%opt%"=="6" (
    start "" "%~dp0omega\command_center\omega_infinity_cockpit.html"
    goto :eof
)
if "%opt%"=="7" (
    exit /b 0
)

echo Invalid choice.
pause
