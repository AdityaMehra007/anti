# GLOBAL CAPITAL OS - PowerShell Launcher
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "           GLOBAL CAPITAL OS (CODENAME: FOUNDER CAPITAL ENGINE)" -ForegroundColor Cyan
Write-Host "                      SOVEREIGN AUTONOMOUS PLATFORM" -ForegroundColor White
Write-Host "                    FOUNDER: ADITYA MEHRA | BENGALURU" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan

Write-Host "`n[1/3] Verifying SQLite WAL Database & Cryptographic Audit Chain..." -ForegroundColor Yellow
python -c "from GLOBAL_CAPITAL_OS.core.database import db; from GLOBAL_CAPITAL_OS.core.audit import audit; print('[OK] Database initialized. Audit chain:', audit.verify_chain_integrity()['message'])"

Write-Host "`n[2/3] Running Automated 3-Way Reconciliation & Anomaly Scan..." -ForegroundColor Yellow
python -c "from GLOBAL_CAPITAL_OS.engines.reconciliation_engine import reconciliation_engine; print('[OK] 3-Way Reconciliation:', reconciliation_engine.execute_three_way_reconciliation()['reconciliation_status'])"

Write-Host "`n[3/3] Launching Executive Command Center on http://127.0.0.1:8000 ..." -ForegroundColor Green
python -m uvicorn GLOBAL_CAPITAL_OS.web.server:app --host 127.0.0.1 --port 8000
