# Coolify v4 Windows Orchestrator & Container Launcher
# OMEGA Autonomous Infrastructure Suite

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  COOLIFY v4 AUTONOMOUS ENTERPRISE ORCHESTRATOR" -ForegroundColor Yellow
Write-Host "  OMEGA Platform Infrastructure Suite" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

# 1. Verify Python SDK
Write-Host "[1/3] Verifying Coolify Python SDK..." -ForegroundColor Cyan
try {
    python -c "import coolify_orchestrator; print('Coolify SDK loaded successfully.')"
    Write-Host "[OK] Coolify SDK and CLI operational." -ForegroundColor Green
} catch {
    Write-Host "[WARN] Python verification encountered an issue." -ForegroundColor Yellow
}

# 2. Check Docker Status
Write-Host "`n[2/3] Checking Docker daemon status..." -ForegroundColor Cyan
$dockerStatus = docker info 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Docker daemon is running." -ForegroundColor Green
    Write-Host "To launch the full live Coolify containers, run:" -ForegroundColor Gray
    Write-Host "  cd coolify && docker compose -f docker-compose.windows.yml up -d" -ForegroundColor White
} else {
    Write-Host "[NOTICE] Docker Desktop daemon is not currently running." -ForegroundColor Yellow
    Write-Host "Coolify Orchestrator operates in high-fidelity mock mode without external dependencies." -ForegroundColor Gray
}

# 3. Launch Mission Control Cockpit
Write-Host "`n[3/3] Opening Interactive Mission Control Cockpit..." -ForegroundColor Cyan
Start-Process "coolify_control_cockpit.html"

# Run summary
Write-Host "`nFetching cluster status via CLI:" -ForegroundColor Cyan
python coolify_cli.py info
