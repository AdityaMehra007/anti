@echo off
setlocal
title Hermes Agent - Web Dashboard

set "HERMES_PYTHON=e:\anti\external\hermes-agent\.venv\Scripts\python.exe"
set "PYTHONIOENCODING=utf-8"

echo =======================================================
echo          STARTING HERMES AGENT WEB DASHBOARD
echo =======================================================
echo Location: http://127.0.0.1:9119
echo.

cd /d "e:\anti\external\hermes-agent"
start http://127.0.0.1:9119
"%HERMES_PYTHON%" -m hermes_cli.main dashboard --skip-build
pause
