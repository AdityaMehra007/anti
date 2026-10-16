@echo off
title Ollama Lean Workstation Launcher (GTX 960M Safe)
echo ======================================================================
echo   OLLAMA LEAN WORKSTATION LAUNCHER
echo   Configured for: NVIDIA GTX 960M (4GB VRAM) & E:\ High-Capacity Storage
echo ======================================================================
echo.

:: Ensure models are saved on E:\ drive, keeping C:\ system SSD free
set "OLLAMA_MODELS=E:\anti gravity\Tools\Ollama\models"
set "OLLAMA_HOST=127.0.0.1:11434"

if not exist "%OLLAMA_MODELS%" (
    echo [*] Creating models storage directory on E:\ partition...
    mkdir "%OLLAMA_MODELS%"
)

echo [*] Models Path: %OLLAMA_MODELS%
echo [*] Service Host: %OLLAMA_HOST%
echo.
echo [*] Starting Ollama local daemon in background...
echo [*] Recommended models: llama3.2:1b or qwen2.5:1.5b (under 2GB VRAM)
echo [*] To pull a lean model: "E:\anti gravity\Tools\Ollama\ollama.exe" run llama3.2:1b
echo.

"E:\anti gravity\Tools\Ollama\ollama.exe" serve
