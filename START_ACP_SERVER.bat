@echo off
setlocal
title Hermes Agent - ACP Server

set "HERMES_PYTHON=e:\anti\external\hermes-agent\.venv\Scripts\python.exe"
set "PYTHONIOENCODING=utf-8"

echo =======================================================
echo          STARTING HERMES AGENT ACP SERVER
echo =======================================================
echo Listening for editor integration (VS Code, Zed, JetBrains)...
echo.

cd /d "e:\anti"
"%HERMES_PYTHON%" -m hermes_cli.main acp
pause
