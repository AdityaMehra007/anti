@echo off
title Blackbird OSINT & Defensive Intelligence Suite CLI
cd /d "%~dp0"

echo ===============================================================================
echo          BLACKBIRD OSINT & DEFENSIVE FOOTPRINT INTELLIGENCE SUITE
echo ===============================================================================
echo [1] Run OSINT Reconnaissance on Username
echo [2] Run Instant Simulation Demo (@octocat)
echo [3] View Platform Census & Category Statistics (692 Sites)
echo [4] Launch Blackbird Mission Control Cockpit (Web UI)
echo [5] Run Original Blackbird CLI
echo [6] Exit
echo ===============================================================================
set /p choice="Select an option (1-6): "

if "%choice%"=="1" (
    set /p target_user="Enter Target Username: "
    python blackbird_cli.py -u %target_user% --audit --export-all
    pause
    goto end
)
if "%choice%"=="2" (
    python blackbird_cli.py --demo
    pause
    goto end
)
if "%choice%"=="3" (
    python blackbird_cli.py --stats
    pause
    goto end
)
if "%choice%"=="4" (
    call START_BLACKBIRD_COCKPIT.bat
    goto end
)
if "%choice%"=="5" (
    set /p orig_user="Enter Username for original Blackbird: "
    python blackbird\blackbird.py -u %orig_user%
    pause
    goto end
)

:end
