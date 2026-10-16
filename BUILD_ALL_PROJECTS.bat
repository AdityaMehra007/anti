@echo off
title Antigravity Workspace Master Multi-Project Builder
echo ======================================================================
echo   ANTIGRAVITY OMNISYSTEM: MASTER MULTI-PROJECT BUILD RUNNER
echo   Builds & Validates 10 Systems (158 Tests): Career Engine, PowerBI Model,
echo   Apex Analytics API, Terra Kinetics SDK, Sovereign Continuum Engine,
echo   TinyAGI TS Core, TradingAgents, AQUA CRM/War Room, BYOX Core, & Telemetry
echo ======================================================================
echo.

python "%~dp0BUILD_ALL_PROJECTS.py"

echo.
pause
