@echo off
setlocal enabledelayedexpansion
title OPENBB OPEN DATA PLATFORM (ODP v5.0.0) — MISSION CONTROL
chcp 65001 >nul
color 0b

set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "OPENBB_AUTO_BUILD=false"
set "REPO_ROOT=%~dp0OpenBB"
if not exist "%REPO_ROOT%" set "REPO_ROOT=%~dp0"
set "PYTHON_EXE=%REPO_ROOT%\.venv\Scripts\python.exe"

:MENU
cls
echo ==============================================================================
echo    OPENBB OPEN DATA PLATFORM (ODP v5.0.0) — SUPREME MISSION CONTROL
echo ==============================================================================
echo.
echo   [1]  Launch OpenBB Python Financial REPL (Interactive obb Session)
echo   [2]  Launch OpenBB Platform REST API Server (port 6900 + Swagger UI)
echo   [3]  Launch OpenBB FastMCP Server for AI Agents (port 8001 / SSE & stdio)
echo   [4]  Launch OpenBB Interactive CLI Terminal (prompt-toolkit shell)
echo   [5]  Launch OpenBB Desktop Frontend (Vite Client on port 1470)
echo   [6]  Run Full System Diagnostics & Verification Suite
echo   [7]  Display Platform Topology & Extensions Inventory
echo   [8]  Sync & Register OpenBB MCP Server with Antigravity / AI Agents
echo   [9]  Exit
echo.
echo ==============================================================================
set /p "CHOICE=Enter selection [1-9]: "

if "%CHOICE%"=="1" goto REPL
if "%CHOICE%"=="2" goto API
if "%CHOICE%"=="3" goto MCP
if "%CHOICE%"=="4" goto CLI
if "%CHOICE%"=="5" goto DESKTOP
if "%CHOICE%"=="6" goto TEST
if "%CHOICE%"=="7" goto INFO
if "%CHOICE%"=="8" goto SYNC_MCP
if "%CHOICE%"=="9" goto EXIT

echo Invalid selection. Please enter 1 to 9.
timeout /t 2 >nul
goto MENU

:REPL
cls
echo Starting Interactive Python Analytics Session...
"%PYTHON_EXE%" "%~dp0openbb_orchestrator.py" repl
pause
goto MENU

:API
cls
echo Starting OpenBB Platform REST API Server...
"%PYTHON_EXE%" "%~dp0openbb_orchestrator.py" serve-api --host 127.0.0.1 --port 6900
pause
goto MENU

:MCP
cls
echo Starting OpenBB Model Context Protocol (MCP) Server...
"%PYTHON_EXE%" "%~dp0openbb_orchestrator.py" serve-mcp --host 127.0.0.1 --port 8001 --transport streamable-http
pause
goto MENU

:CLI
cls
echo Starting OpenBB Platform Interactive CLI...
"%PYTHON_EXE%" "%~dp0openbb_orchestrator.py" cli
pause
goto MENU

:DESKTOP
cls
echo Starting OpenBB Desktop Web Frontend...
"%PYTHON_EXE%" "%~dp0openbb_orchestrator.py" desktop-dev --port 1470
pause
goto MENU

:TEST
cls
echo Running Automated Platform Health Verification...
"%PYTHON_EXE%" "%~dp0openbb_orchestrator.py" test
pause
goto MENU

:INFO
cls
echo Gathering Platform Inventory and Topology...
"%PYTHON_EXE%" "%~dp0openbb_orchestrator.py" info
pause
goto MENU

:SYNC_MCP
cls
echo Registering and Syncing OpenBB MCP Server with Antigravity...
"%PYTHON_EXE%" "%~dp0OpenBB\register_openbb_mcp.py"
pause
goto MENU

:EXIT
echo Exiting OpenBB Mission Control. Goodbye!
exit /b 0
