@echo off
title CIVILIZATION OMEGA PLANETARY AGENT SWARM
cd /d %~dp0
echo ==============================================================================
echo [CIVILIZATION OMEGA] ACTIVATING PLANETARY AGENT SWARM (10 NODES, 166 AGENTS)
echo ==============================================================================
python planetary_agent_hive.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Planetary swarm dispatch encountered an issue.
    pause
    exit /b %ERRORLEVEL%
)
echo [OK] Launching Planetary Cockpit Dashboard...
start "" "planetary_agent_hive_dashboard.html"
pause
