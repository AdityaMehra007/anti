@echo off
title Antigravity Career OS - FastAPI Server
cd /d "%~dp0projects\flagship-career-engine"
echo ======================================================================
echo   STARTING ANTIGRAVITY REST API SERVER (Port 8080)
echo   Endpoints: http://127.0.0.1:8080/
echo   Interactive Swagger Docs: http://127.0.0.1:8080/docs
echo ======================================================================
python api_server.py
pause
