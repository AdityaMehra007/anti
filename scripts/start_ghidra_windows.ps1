<#
.SYNOPSIS
    Launches NSA Ghidra Autonomous SRE Suite and opens Mission Control Cockpit on Windows.
.DESCRIPTION
    Executes the 12-phase sovereign lifecycle, verifies attestation, starts the API bridge
    on port 8770, and launches the browser cockpit.
#>

param(
    [int]$Port = 8771,
    [switch]$SkipLifecycle = $false
)

Write-Host "===============================================================================" -ForegroundColor Green
Write-Host "  NSA GHIDRA SOVEREIGN AUTONOMOUS SUITE (github.com/NationalSecurityAgency/ghidra)" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Green
Write-Host ""

if (-not $SkipLifecycle) {
    Write-Host "[*] Executing 12-Phase Sovereign SRE Lifecycle..." -ForegroundColor Cyan
    python ghidra_cli.py do-everything
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Lifecycle attestation reported non-zero exit code."
    }
}

Write-Host "[*] Starting NSA Ghidra Autonomous API Server on port $Port..." -ForegroundColor Cyan
Start-Process "http://localhost:$Port/"

python ghidra_api_server.py --port $Port
