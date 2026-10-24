@echo off
TITLE OMEGA ∞ Supreme Sovereign Command Suite
cd /d "%~dp0"
echo ===============================================================================
echo        OMEGA ∞ SUPREME SOVEREIGN ENTERPRISE COMMAND SUITE v24.0
echo ===============================================================================
echo.
echo [*] Starting OMEGA Omniverse REST API Server on http://127.0.0.1:8900 ...
start "OMEGA Omniverse REST API" cmd /k "python omega_omniverse_api.py"

timeout /t 2 /nobreak >nul

echo [*] Opening Supreme Sovereign Command Center in Browser ...
start "" "omega_supreme_command_center.html"

echo [*] Opening 546-Account Commercial Deal Cockpit ...
start "" "bangalore_enterprise_deal_cockpit.html"

echo.
echo ===============================================================================
echo   ALL 5 SOVEREIGN ENTERPRISE ENGINES ONLINE:
echo   1. Supreme Command Center:   file:///%CD:\=/%/omega_supreme_command_center.html
echo   2. Bangalore Top 500:        file:///%CD:\=/%/bangalore_top_500_cockpit.html
echo   3. 546-Account Deal CRM:     file:///%CD:\=/%/bangalore_enterprise_deal_cockpit.html
echo   4. Fortune 500 Factory:      file:///%CD:\=/%/fortune_500_cockpit.html
echo   5. Omniverse REST API:       http://127.0.0.1:8900/docs
echo   6. Quality Gateway (124+ T): python VERIFY_ALL_PROJECT_TESTS.py
echo ===============================================================================
echo.
pause
