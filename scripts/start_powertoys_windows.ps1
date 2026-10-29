<#
.SYNOPSIS
  PowerToys Sovereign Autonomous Suite Launcher (PowerShell)
.DESCRIPTION
  Executes the 12-phase sovereign lifecycle attestation and boots the API bridge / Cockpit.
#>

[CmdletBinding()]
param(
    [int]$Port = 8770,
    [switch]$SkipLifecycle
)

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "  MICROSOFT POWERTOYS SOVEREIGN AUTONOMOUS SUITE (github.com/microsoft/PowerToys)" -ForegroundColor Cyan
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

if (-not $SkipLifecycle) {
    Write-Host "[1/2] Executing 12-Phase Sovereign PowerToys Lifecycle..." -ForegroundColor Yellow
    python powertoys_cli.py do-everything
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "PowerToys 12-Phase lifecycle reported non-zero status code."
    }
}

Write-Host "[2/2] Launching Local API Bridge & Mission Control Cockpit on port $Port..." -ForegroundColor Green
Start-Process "http://localhost:$Port/cockpit"
python powertoys_api_server.py --port $Port
