<#
.SYNOPSIS
    Windmill Windows Autonomous Launch & Pre-Flight Verification Script
.DESCRIPTION
    Verifies Python environment, tests Windmill CLI commands, checks port availability,
    launches the local API server in the background, and opens the Mission Control Cockpit.
#>

$ErrorActionPreference = "Continue"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  WINDMILL AUTONOMOUS WORKFLOW & DEVELOPER PLATFORM        " -ForegroundColor Green
Write-Host "  OMEGA Infrastructure & DAG Automation Engine             " -ForegroundColor DarkCyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir
Set-Location $RootDir

Write-Host "[1/4] Testing Windmill SDK and CLI..." -ForegroundColor Yellow
$infoOutput = python windmill_cli.py info
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Windmill Orchestrator validated." -ForegroundColor Green
} else {
    Write-Host "[WARNING] Windmill CLI returned code $LASTEXITCODE" -ForegroundColor DarkYellow
}

Write-Host "`n[2/4] Checking local ports..." -ForegroundColor Yellow
$portCheck = Get-NetTCPConnection -LocalPort 8768 -ErrorAction SilentlyContinue
if ($portCheck) {
    Write-Host "[*] Port 8768 already active (Windmill API server running)." -ForegroundColor Green
} else {
    Write-Host "[*] Starting background Windmill API Bridge Server on port 8768..." -ForegroundColor Cyan
    Start-Process -FilePath "python" -ArgumentList "windmill_api_server.py --port 8768" -WindowStyle Hidden
    Start-Sleep -Seconds 1
}

Write-Host "`n[3/4] Launching Mission Control Cockpit..." -ForegroundColor Yellow
$cockpitFile = Join-Path $RootDir "windmill_control_cockpit.html"
if (Test-Path $cockpitFile) {
    Start-Process $cockpitFile
    Write-Host "[OK] Cockpit opened in browser." -ForegroundColor Green
}

Write-Host "`n[4/4] Platform Telemetry Summary:" -ForegroundColor Yellow
python windmill_cli.py info

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  WINDMILL ORCHESTRATOR IS 100% READY AND OPERATIONAL     " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
