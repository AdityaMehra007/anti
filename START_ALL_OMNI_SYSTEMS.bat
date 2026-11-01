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

echo [*] Starting Blackbird OSINT & Defensive Intelligence Server on http://127.0.0.1:8777...
start "Blackbird OSINT API Server" cmd /k "python blackbird_orchestrator.py --serve 8777"

echo [*] Starting Windmill Autonomous Workflow & Developer Platform Server on http://127.0.0.1:8768...
start "Windmill API Server" cmd /k "python windmill_api_server.py --port 8768"

echo [*] Starting PowerShell Autonomous Ecosystem Server on http://127.0.0.1:8769...
start "PowerShell API Server" cmd /k "python powershell_api_server.py --port 8769"

echo [*] Starting Microsoft PowerToys Autonomous Suite Server on http://127.0.0.1:8770...
start "PowerToys API Server" cmd /k "python powertoys_api_server.py --port 8770"

echo [*] Starting NSA Ghidra Autonomous SRE Suite Server on http://127.0.0.1:8771...
start "Ghidra API Server" cmd /k "python ghidra_api_server.py --port 8771"

echo [*] Starting Free-for-Dev Autonomous Cloud Intelligence on http://127.0.0.1:8772...
start "Free-For-Dev API Server" cmd /k "python free_for_dev_api_server.py --port 8772"

echo [*] Starting Infisical Autonomous SecretOps Platform on http://127.0.0.1:8773...
start "Infisical API Server" cmd /k "python infisical_api_server.py --port 8773"

echo [*] Starting Plane CE Autonomous Project & Issue Engine on http://127.0.0.1:8774...
start "Plane API Server" cmd /k "python plane_api_server.py --port 8774"

echo [*] Starting Apache Airflow Autonomous Orchestration Server on http://127.0.0.1:8775...
start "Airflow API Server" cmd /k "python airflow_api_server.py --port 8775"

echo [*] Starting Apache Arrow In-Memory Columnar Engine on http://127.0.0.1:8776...
start "Arrow API Server" cmd /k "python arrow_api_server.py --port 8776"

echo [*] Starting n8n Autonomous Workflow Automation on http://127.0.0.1:8778...
start "n8n API Server" cmd /k "python n8n_api_server.py --port 8778"

echo [*] Starting CS Video Courses Academic Intelligence on http://127.0.0.1:8779...
start "CS Courses API Server" cmd /k "python cs_courses_api_server.py 8779"

echo [*] Starting Hiring Without Whiteboards Autonomous Cockpit on http://127.0.0.1:8780...
start "Hiring Without Whiteboards API Server" cmd /k "python hiring_without_whiteboards_engine.py --serve 8780"

timeout /t 2 /nobreak >nul

echo [*] Launching Master Executive Mission Control in browser...
start "" "OMNI_EXECUTIVE_COCKPIT.html"

echo ==============================================================================
echo   ALL SYSTEMS ONLINE:
echo   1.  Master Executive Cockpit: file:///e:/anti/OMNI_EXECUTIVE_COCKPIT.html
echo   2.  Universal Job & Skill API: http://127.0.0.1:8765
echo   3.  prompts.chat Studio API:  http://127.0.0.1:8877
echo   4.  Coolify PaaS & Cockpit:   http://127.0.0.1:8767
echo   5.  Windmill Workflow Engine: http://127.0.0.1:8768
echo   6.  PowerShell Ecosystem API: http://127.0.0.1:8769
echo   7.  PowerToys Suite API:      http://127.0.0.1:8770
echo   8.  NSA Ghidra SRE API:       http://127.0.0.1:8771
echo   9.  Free-for-Dev Cloud API:   http://127.0.0.1:8772
echo   10. Infisical SecretOps API:  http://127.0.0.1:8773
echo   11. Plane CE Issue API:       http://127.0.0.1:8774
echo   12. Apache Airflow API:       http://127.0.0.1:8775
echo   13. Apache Arrow Engine API:  http://127.0.0.1:8776
echo   14. Blackbird OSINT Cockpit:  http://127.0.0.1:8777
echo   15. n8n Automation Engine:    http://127.0.0.1:8778
echo   16. CS Video Courses Cockpit: http://127.0.0.1:8779
echo   17. Hiring Without Whiteboard:http://127.0.0.1:8780
echo   18. 7-Agent APEX Cockpit:     file:///e:/anti/apex_career_cockpit.html
echo   19. Global Opportunity Map:   file:///e:/anti/master_job_universe_dashboard.html
echo ==============================================================================
pause
