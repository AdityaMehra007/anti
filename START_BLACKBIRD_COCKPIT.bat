@echo off
title Blackbird OSINT Mission Control Cockpit
cd /d "%~dp0"

echo [i] Starting Blackbird OSINT Mission Control Cockpit on port 8777...
start "" http://127.0.0.1:8777/blackbird_cockpit.html
python blackbird_orchestrator.py --serve 8777
pause
