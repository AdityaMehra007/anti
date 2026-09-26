@echo off
title CLAUDE CODE CLI — OMNIROUTE GATEWAY
color 0B

echo ============================================================
echo   LAUNCHING CLAUDE CODE CLI VIA OMNIROUTE (PORT 20128)
echo ============================================================
echo.

set ANTHROPIC_BASE_URL=http://localhost:20128/v1
set ANTHROPIC_API_KEY=sk-47d56e1c83c613b8-340fcd-4b5d015f
set OMNIROUTE_API_KEY=sk-47d56e1c83c613b8-340fcd-4b5d015f

echo Routing Claude Code to: %ANTHROPIC_BASE_URL%
echo.

"C:\Users\amehr\.local\bin\claude.exe" %*
