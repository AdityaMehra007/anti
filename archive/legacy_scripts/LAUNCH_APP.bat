@echo off
TITLE GLOBAL DOLLAR ECONOMY OS - WEB APP LAUNCHER
COLOR 0B

:: ============================================================================
:: GLOBAL DOLLAR ECONOMY OS -- WEB APP LAUNCHER
:: Founder: Adi | Base: Bangalore, India
:: ============================================================================

cd /d "E:\anti"

echo ============================================================================
echo   STARTING GLOBAL DOLLAR ECONOMY OS INTERACTIVE WEB DASHBOARD
echo ============================================================================
echo.
echo   Local URL: http://localhost:8000
echo.
echo   Opening dashboard in default web browser...
echo.

start "" "http://localhost:8000"

python app.py

pause
