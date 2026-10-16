@echo off
TITLE ADITYA APEX CAREER SUITE — All-in-One Flagship Launcher
COLOR 0A

echo ===============================================================================
echo            ADITYA APEX CAREER SUITE -- ALL-IN-ONE FLAGSHIP COCKPIT
echo ===============================================================================
echo Candidate : Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
echo System    : Flagship 9-Tab Unified SPA Career Cockpit
echo Guardrail : 100%% Evidence-Verified | 1-Click Clipboard Dispatch
echo ===============================================================================
echo.
echo [*] Checking Hermes Autonomous Controller daemon (Port 9119)...
curl -s http://127.0.0.1:9119/ > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] Hermes controller daemon not detected on port 9119.
    echo [*] Starting Hermes controller daemon in background...
    start /min python HERMES_AUTONOMOUS_CONTROLLER.py
    timeout /t 2 /nobreak > nul
) else (
    echo [OK] Hermes controller daemon active on http://127.0.0.1:9119.
)

echo [*] Launching Flagship APEX Career Suite in default browser...
start "" "%~dp0ADITYA_APEX_CAREER_SUITE.html"

echo.
echo [DONE] Apex Suite is running. You can keep this window open or close it.
echo Press any key to exit.
pause > nul
