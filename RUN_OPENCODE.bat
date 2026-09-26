@echo off
title OpenCode Agentic Command Center
color 0B
echo ===============================================================================
echo            OPENCODE (ANOMALYCO) AUTONOMOUS AGENT LAUNCHER
echo ===============================================================================
echo [INFO] Workspace: E:\anti
echo [INFO] Dual Modes: 'build' (execution) ^| 'plan' (analysis)
echo [INFO] Subagent: @general
echo ===============================================================================

set "PATH=E:\anti gravity\npm-global;%PATH%"

where opencode >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Launching OpenCode CLI v1.18.29...
    opencode %*
) else (
    if exist "E:\anti gravity\npm-global\opencode.cmd" (
        echo [OK] Launching OpenCode via npm-global...
        call "E:\anti gravity\npm-global\opencode.cmd" %*
    ) else (
        echo [NOTICE] OpenCode executable not found.
    )
)
pause
