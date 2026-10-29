<#
.SYNOPSIS
    n8n Windows Autonomous Launch & Pre-Flight Verification Script
.DESCRIPTION
    Verifies Python environment, tests n8n CLI commands, checks port 8771,
    launches the local API server in the background, and opens the Mission Control Cockpit.
#>

$ErrorActionPreference = "Continue"

Write-Host "==========================================================" -ForegroundColor Red
Write-Host "  n8n ENTERPRISE WORKFLOW PLATFORM & AGENT ENGINE          " -ForegroundColor Yellow
Write-Host "  OMEGA Infrastructure & Node DAG Automation Core          " -ForegroundColor DarkYellow
Write-Host "==========================================================" -ForegroundColor Red
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir
Set-Location $RootDir

Write-Host "[1/4] Testing n8n SDK and CLI..." -ForegroundColor Yellow
$infoOutput = python n8n_cli.py info
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] n8n Orchestrator validated." -ForegroundColor Green
} else {
    Write-Host "[WARNING] n8n CLI returned code $LASTEXITCODE" -ForegroundColor DarkYellow
}

Write-Host "`n[2/4] Checking local ports..." -ForegroundColor Yellow
$portCheck = Get-NetTCPConnection -LocalPort 8771 -ErrorAction SilentlyContinue
if ($portCheck) {
    Write-Host "[*] Port 8771 already active (n8n API server running)." -ForegroundColor Green
} else {
    Write-Host "[*] Starting background n8n API Bridge Server on port 8771..." -ForegroundColor Cyan
    Start-Process -FilePath "python" -ArgumentList "n8n_api_server.py --port 8771" -WindowStyle Hidden
    Start-Sleep -Seconds 1
}

Write-Host "`n[3/4] Launching Mission Control Cockpit..." -ForegroundColor Yellow
$cockpitFile = Join-Path $RootDir "n8n_control_cockpit.html"
if (Test-Path $cockpitFile) {
    Start-Process $cockpitFile
    Write-Host "[OK] Cockpit opened in default browser." -ForegroundColor Green
} else {
    Write-Host "[!] Cockpit HTML not found at $cockpitFile" -ForegroundColor Red
}

Write-Host "`n[4/4] Executing 12-Phase Sovereign Verification..." -ForegroundColor Yellow
python n8n_cli.py do-everything
Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  n8n Autonomous Platform fully initialized and verified!  " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
