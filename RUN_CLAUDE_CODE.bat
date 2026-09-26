@echo off
TITLE ADI CAREER OS — Claude Code Terminal Bridge
COLOR 0B

echo ===============================================================================
echo            ADI CAREER OS -- CLAUDE CODE AUTONOMOUS AGENT BRIDGE
echo ===============================================================================
echo Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
echo Workspace: e:\anti
echo Context:   e:\anti\CLAUDE.md
echo ===============================================================================
echo.
echo [1] 1-Click Login to Claude (Opens Browser OAuth -- Fast & Free)
echo [2] Launch Interactive Claude Code Session
echo [3] Run System Health Diagnostics (claude doctor)
echo [4] Verify Environment & Auth Status
echo [5] Exit
echo.
set /p choice="Select an option (1-5): "

if "%choice%"=="1" (
    echo.
    echo Starting Claude Code Auth Login for adityamehra799@gmail.com...
    claude auth login --email adityamehra799@gmail.com
    pause
    goto end
)
if "%choice%"=="2" (
    echo Launching Claude Code...
    claude
    goto end
)
if "%choice%"=="3" (
    echo Running Claude Code Diagnostics...
    claude doctor
    pause
    goto end
)
if "%choice%"=="4" (
    python scripts/run_claude_code.py
    pause
    goto end
)

:end

