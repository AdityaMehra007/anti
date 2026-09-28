@echo off
title OMEGA ∞ (Ω-OS) — Sovereign Enterprise Operating System
cd /d %~dp0

echo ======================================================================
echo   OMEGA ∞ (Ω-OS) — SOVEREIGN ENTERPRISE OPERATING SYSTEM
echo   Constitutional Governance & Autonomous Enterprise Infrastructure
echo   Entity: VECTIS TRADE TECHNOLOGIES PRIVATE LIMITED (Bengaluru, India)
echo ======================================================================
echo.

echo [1/4] Running Comprehensive Verification Test Suite...
pytest tests/test_omega_infinity.py -v
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Verification tests failed! Aborting startup.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/4] Initializing Sovereign Kernel & Cryptographic Ledger...
python -c "from omega_infinity.omega_infinity_core import get_kernel; k = get_kernel(); print('Ledger Verified:', k.ledger.verify_integrity()['valid'])"

echo.
echo [3/5] Ensuring Sample Trade Dockets & Ingestion Queues Active...
python -c "from company.vectis_parser import generate_sample_dockets; generate_sample_dockets()"

echo.
echo [4/5] Compiling Daily Sovereign Executive Brief...
python omega_infinity/omega_daily_brief.py

echo.
echo [5/5] Launching Glass Cockpit Web Server on http://localhost:8888...
start http://localhost:8888
python omega_cli.py serve --port 8888

pause
