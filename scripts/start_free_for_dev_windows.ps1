<#
.SYNOPSIS
    Starts the OMEGA Free-For-Dev Developer Cloud API Server and Cockpit on Windows.
.DESCRIPTION
    Attests catalog integrity, checks port 8770, starts the API server in background,
    and opens the Mission Control Cockpit in the default browser.
#>

[CmdletBinding()]
param(
    [int]$Port = 8771,
    [switch]$NoBrowser
)

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "  FREE-FOR-DEV SOVEREIGN DEVELOPER CLOUD (github.com/ripienaar/free-for-dev)" -ForegroundColor Cyan
Write-Host "  OMEGA Autonomous Zero-Dollar Architecture & Quota Engine" -ForegroundColor Cyan
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

$WorkspaceRoot = Split-Path -Parent $PSScriptRoot
Set-Location $WorkspaceRoot

Write-Host "[1/3] Executing 12-Phase Sovereign Lifecycle..." -ForegroundColor Yellow
python free_for_dev_cli.py do-everything
if ($LASTEXITCODE -ne 0) {
    Write-Error "Sovereign Lifecycle failed."
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/3] Checking Port $Port and starting API Server..." -ForegroundColor Yellow
$PortBound = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue

if ($PortBound) {
    Write-Host "[NOTICE] Port $Port is already bound. Assuming Free-For-Dev API Server is online." -ForegroundColor Green
} else {
    Start-Process -FilePath "python" -ArgumentList "free_for_dev_api_server.py $Port" -WindowStyle Hidden
    Start-Sleep -Seconds 2
    Write-Host "[OK] API Server started in background on http://localhost:$Port" -ForegroundColor Green
}

if (-not $NoBrowser) {
    Write-Host ""
    Write-Host "[3/3] Opening Mission Control Cockpit..." -ForegroundColor Yellow
    Start-Process "http://localhost:$Port"
}

Write-Host ""
Write-Host "[SUCCESS] Free-For-Dev Developer Cloud operational on http://localhost:$Port" -ForegroundColor Cyan
