@echo off
title OMEGA UNIVERSAL JOB & SKILL INTELLIGENCE COCKPIT
cd /d "e:\anti"
echo ==============================================================================
echo   OMEGA UNIVERSAL JOB & SKILL INTELLIGENCE COCKPIT
echo   Universal Taxonomy Dissector, Skill Builder & 500+ Opportunity Census
echo ==============================================================================
echo [*] Launching Cockpit Server at http://127.0.0.1:8765...
start http://127.0.0.1:8765
python universal_jd_intelligence_engine.py --serve-cockpit 8765
pause
