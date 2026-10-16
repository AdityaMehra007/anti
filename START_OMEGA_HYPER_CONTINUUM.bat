@echo off
title OMEGA HYPER-CONTINUUM COMMAND CENTER
cd /d %~dp0
echo ==============================================================================
echo [OMEGA] LAUNCHING HYPER-CONTINUUM (SKILLS • JOBS • AGENTS • FUNDS)
echo ==============================================================================
python omega_hyper_continuum.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Hyper-Continuum synthesis failed.
    pause
    exit /b %ERRORLEVEL%
)
echo [OK] Opening Sovereign Hyper-Continuum Dashboard...
start "" "omega_hyper_continuum_dashboard.html"
pause
