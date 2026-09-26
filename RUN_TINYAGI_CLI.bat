@echo off
title TinyAGI CLI Console
cd /d "e:\anti\tinyagi"
echo =======================================================
echo   TinyAGI CLI Console
echo   Examples:
echo     tinyagi agent list
echo     tinyagi team list
echo     tinyagi status
echo =======================================================
if "%~1"=="" (
    cmd /k "node packages/cli/bin/tinyagi.mjs --help"
) else (
    node packages/cli/bin/tinyagi.mjs %*
)
