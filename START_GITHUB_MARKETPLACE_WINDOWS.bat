@echo off
title GitHub Marketplace Sovereign Autonomous Suite Launcher
color 0b
echo ===============================================================================
echo   GITHUB MARKETPLACE SOVEREIGN AUTONOMOUS SUITE (https://github.com/marketplace)
echo ===============================================================================
echo.
echo Executing 12-Phase Sovereign Lifecycle & Attestation...
python github_marketplace_cli.py do-everything
echo.
echo Starting GitHub Marketplace API Server on http://127.0.0.1:8783...
start "GitHub Marketplace API Server" cmd /k "python github_marketplace_api_server.py 8783"
timeout /t 2 /nobreak >nul
echo.
echo Launching Interactive Mission Control Cockpit...
start "" "github_marketplace_cockpit.html"
echo.
pause
