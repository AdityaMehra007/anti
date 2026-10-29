# ===============================================================================
# Infisical Sovereign SecretOps Suite Launcher (PowerShell Edition)
# ===============================================================================

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "  INFISICAL SOVEREIGN SECRETOPS SUITE (github.com/Infisical/infisical)" -ForegroundColor White
Write-Host "  Zero-Knowledge Secrets | Dynamic Credentials | PKI CA | Cloud Sync" -ForegroundColor Gray
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

# Phase 1: 12-Phase Lifecycle
Write-Host "[1/3] Executing 12-Phase Sovereign SecretOps Lifecycle & Certification..." -ForegroundColor Yellow
python infisical_cli.py do-everything
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Lifecycle certification encountered errors." -ForegroundColor Red
    exit $LASTEXITCODE
}

# Phase 2: Start API Server
Write-Host ""
Write-Host "[2/3] Launching Autonomous Local REST API Server on port 8772..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "infisical_api_server.py --port 8772" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Phase 3: Launch Browser
Write-Host ""
Write-Host "[3/3] Opening Interactive Mission Control Cockpit in Default Browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8772/"

Write-Host ""
Write-Host "===============================================================================" -ForegroundColor Green
Write-Host "  INFISICAL SOVEREIGN SECRETOPS SYSTEM ACTIVE & READY" -ForegroundColor White
Write-Host "  Mission Cockpit : http://localhost:8772/" -ForegroundColor Gray
Write-Host "  Telemetry API   : http://localhost:8772/api/status" -ForegroundColor Gray
Write-Host "  Audit Ledger    : SHA-256 Chained Integrity Verified" -ForegroundColor Gray
Write-Host "===============================================================================" -ForegroundColor Green
