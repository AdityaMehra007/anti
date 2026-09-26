@echo off
title GLOBAL CAPITAL OS - Founder Capital Engine
echo ===============================================================================
echo            GLOBAL CAPITAL OS (CODENAME: FOUNDER CAPITAL ENGINE)
echo                       SOVEREIGN AUTONOMOUS PLATFORM
echo                     FOUNDER: ADITYA MEHRA | BENGALURU
echo ===============================================================================
echo.
echo [1/3] Verifying SQLite WAL Database & Cryptographic Audit Chain...
python -c "from GLOBAL_CAPITAL_OS.core.database import db; from GLOBAL_CAPITAL_OS.core.audit import audit; print('[OK] Database initialized. Audit chain:', audit.verify_chain_integrity()['message'])"
echo.
echo [2/3] Running Automated 3-Way Reconciliation & Anomaly Scan...
python -c "from GLOBAL_CAPITAL_OS.engines.reconciliation_engine import reconciliation_engine; print('[OK] 3-Way Reconciliation:', reconciliation_engine.execute_three_way_reconciliation()['reconciliation_status'])"
echo.
echo [3/3] Launching Executive Command Center on http://127.0.0.1:8000 ...
python -m uvicorn GLOBAL_CAPITAL_OS.web.server:app --host 127.0.0.1 --port 8000
pause
