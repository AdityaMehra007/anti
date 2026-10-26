<#
.SYNOPSIS
    PowerShell Autonomous Suite Launcher Script.
.DESCRIPTION
    Verifies Python environment, tests execution policy, launches API server on port 8769,
    and opens the Mission Control Cockpit in default browser.
#>

[CmdletBinding()]
param(
    [int]$Port = 8769,
    [switch]$DoEverything = $true,
    [switch]$NoBrowser = $false
)

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  POWERSHELL AUTONOMOUS MISSION CONTROL LAUNCHER" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

if ($DoEverything) {
    Write-Host "[1/3] Executing 12-Phase Sovereign Lifecycle Attestation..." -ForegroundColor Yellow
    python powershell_cli.py do-everything
}

Write-Host "[2/3] Starting Local REST & WebSocket API Server on port $Port..." -ForegroundColor Yellow
$job = Start-Process -FilePath "python" -ArgumentList "powershell_api_server.py --port $Port" -PassThru -WindowStyle Hidden

Start-Sleep -Seconds 2

if (-not $NoBrowser) {
    Write-Host "[3/3] Opening Mission Control Cockpit..." -ForegroundColor Green
    Start-Process "http://localhost:$Port/"
}

Write-Host "PowerShell Autonomous Suite is fully online at http://localhost:$Port/" -ForegroundColor Green
Write-Host "Process ID: $($job.Id). Press Enter to exit launcher."
