@echo off
title AI Command Center Web Cockpit Server
echo ======================================================================
echo   STARTING LOCAL AI COMMAND CENTER SERVER (PORT 8080)
echo ======================================================================
echo.
echo [*] Local URL: http://localhost:8080/projects/flagship-career-engine/
echo [*] Press Ctrl+C in this console window to stop the server when done.
echo.

start "" "http://localhost:8080/projects/flagship-career-engine/"
python -m http.server 8080 --directory "%~dp0"
