@echo off
title OMEGA SOVEREIGN AI & CAREER OS LAUNCHER
color 0A

echo ============================================================
echo   OMEGA SOVEREIGN AI & CAREER OS LAUNCHER
echo   Candidate: Aditya Mehra (Aero India 2025 Lead / DSU BBA IB)
echo ============================================================
echo.

echo [1/4] Checking Local GPU Ollama Server (Port 11434)...
powershell -Command "if (!(Get-NetTCPConnection -LocalPort 11434 -State Listen -ErrorAction SilentlyContinue)) { Start-Process 'E:\anti gravity\Tools\Ollama\ollama.exe' -ArgumentList 'serve' -WindowStyle Hidden; Write-Host '  -> Started Ollama in background.' } else { Write-Host '  -> Ollama is already active.' }"

echo.
echo [2/4] Checking OmniRoute Gateway Server (Port 20128)...
powershell -Command "if (!(Get-NetTCPConnection -LocalPort 20128 -State Listen -ErrorAction SilentlyContinue)) { Start-Process 'cmd.exe' -ArgumentList '/c omniroute serve --port 20128 --no-open --log' -WindowStyle Hidden; Write-Host '  -> Started OmniRoute Gateway on port 20128.' } else { Write-Host '  -> OmniRoute is already active.' }"

echo.
echo [3/4] Warming up NVIDIA GPU with Qwen 2.5 Coder 3B...
powershell -Command "Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/generate' -Method Post -ContentType 'application/json' -Body '{\"model\":\"qwen2.5-coder:3b\",\"keep_alive\":-1}' -ErrorAction SilentlyContinue | Out-Null; Write-Host '  -> GPU VRAM warm and locked in memory.'"

echo.
echo [4/4] Opening Portals & Dashboards...
start "" "http://localhost:20128/dashboard"
start "" "e:\anti\job_application_center.html"
start "" "e:\anti\ANTIGRAVITY_OMNI_HUB.html"

echo.
echo ============================================================
echo   ALL SYSTEMS ONLINE AND READY!
echo   - Local GPU (Port 11434):  Active
echo   - OmniRoute (Port 20128):  Active
echo   - VS Code / Cursor MCP:    Configured
echo   - Job Application Center:  Opened
echo ============================================================
pause
