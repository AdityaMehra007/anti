@echo off
title OMEGA ∞ MCP MASTER MISSION CONTROL HUB
color 0B
cls
echo ======================================================================
echo    OMEGA MODEL CONTEXT PROTOCOL (MCP) MASTER COCKPIT ^& HUB v3.0
echo ======================================================================
echo   Fleet Size : 24 Registered MCP Servers
echo   Tool Count : 260 Schema-Validated Autonomous Tools
echo   Transports : JSON-RPC 2.0 stdio, SSE, and HTTP REST Bridge
echo ======================================================================
echo.

cd /d "E:\anti"

echo [1/3] Generating Latest MCP Catalog...
python scripts\build_mcp_catalog.py
echo.

echo [2/3] Registered Server Fleet:
python mcp_cli.py list
echo.

echo [3/3] Launching Master Cockpit Server on http://localhost:8790 ...
start "" "http://localhost:8790"

python mcp_cli.py serve --port 8790
pause
