@echo off
TITLE OMEGA Global Markets, Business Empire & EXIM Nexus
echo ===============================================================================
echo        OMEGA GLOBAL MARKETS, BUSINESS EMPIRE & EXIM NEXUS v24.0
echo ===============================================================================
echo.
echo Launching FastAPI Server on http://localhost:8800 ...
echo Opening Browser Cockpit ...
echo.

start "" "http://localhost:8800"
python -m projects.omega_global_markets_nexus.run_server

pause
