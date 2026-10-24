@echo off
title prompts.chat Cockpit & Local API Server
echo =================================================================
echo  Launching prompts.chat Local Intelligence Engine & Web Cockpit
echo =================================================================
echo.

start "" http://localhost:8877/
python prompts_chat_cli.py --serve 8877

pause
