@echo off
title OMEGA OMNIVERSE — MASTER SYSTEM LAUNCHER
cd /d "e:\anti"
echo ==============================================================================
echo   OMEGA OMNIVERSE: UNIFIED MASTER SYSTEM LAUNCHER
echo   Candidate: Aditya Mehra | Bengaluru GCC / MNC Operations Track
echo ==============================================================================
echo [*] Starting Universal Job & Skill Cockpit Server on http://127.0.0.1:8765...
start "OMEGA API Server" cmd /k "python universal_jd_intelligence_engine.py --serve-cockpit 8765"

echo [*] Starting prompts.chat Prompt Intelligence Server on http://127.0.0.1:8877...
start "Prompts.chat API Server" cmd /k "python prompts_chat_cli.py --serve 8877"

echo [*] Starting Coolify Autonomous PaaS & Cockpit API Server on http://127.0.0.1:8767...
start "Coolify API Server" cmd /k "python coolify_api_server.py --port 8767"

timeout /t 2 /nobreak >nul

echo [*] Launching Master Executive Mission Control in browser...
start "" "OMNI_EXECUTIVE_COCKPIT.html"

echo ==============================================================================
echo   ALL SYSTEMS ONLINE:
echo   1. Master Executive Cockpit: file:///e:/anti/OMNI_EXECUTIVE_COCKPIT.html
echo   2. Universal Job & Skill API: http://127.0.0.1:8765
echo   3. prompts.chat Studio API:  http://127.0.0.1:8877
echo   4. Coolify PaaS & Cockpit:   http://127.0.0.1:8767
echo   5. 7-Agent APEX Cockpit:     file:///e:/anti/apex_career_cockpit.html
echo   6. Global Opportunity Map:   file:///e:/anti/master_job_universe_dashboard.html
echo ==============================================================================
pause
