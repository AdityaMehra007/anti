@echo off
setlocal
set PYTHONIOENCODING=utf-8
"e:\anti\external\hermes-agent\.venv\Scripts\python.exe" -m hermes_cli.main --tui %*
