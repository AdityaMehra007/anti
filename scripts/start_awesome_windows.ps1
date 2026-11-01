<#
.SYNOPSIS
    Starts the OMEGA Awesome Universe Autonomous Engine & Mission Control Cockpit on Windows.
.DESCRIPTION
    Executes the 12-Phase Sovereign Lifecycle, compiles SQLite FTS5 database,
    opens the interactive dark glassmorphism cockpit, and binds the REST API server on port 8782.
#>

[CmdletBinding()]
param(
    [int]$Port = 8782,
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"
$WorkspaceDir = Split-Path -Parent $PSScriptRoot

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "  GITHUB AWESOME UNIVERSE (github.com/topics/awesome & sindresorhus/awesome)" -ForegroundColor White
Write-Host "  OMEGA Sovereign Curated Knowledge & Manifesto Linter Cockpit" -ForegroundColor Yellow
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location $WorkspaceDir

Write-Host "[1/3] Attesting Universe & Executing 12-Phase Sovereign Lifecycle..." -ForegroundColor Green
python awesome_orchestrator.py

if (-not $NoBrowser) {
    Write-Host "`n[2/3] Launching Mission Control Cockpit in default browser..." -ForegroundColor Green
    $CockpitPath = Join-Path $WorkspaceDir "awesome_control_cockpit.html"
    Start-Process $CockpitPath
}

Write-Host "`n[3/3] Starting Autonomous REST API Server on port $Port..." -ForegroundColor Green
Write-Host "      API Health:  http://127.0.0.1:$Port/api/info" -ForegroundColor White
Write-Host "      Cockpit:     http://127.0.0.1:$Port/cockpit" -ForegroundColor White
Write-Host "`nPress Ctrl+C to terminate the API server." -ForegroundColor DarkGray
Write-Host "===============================================================================" -ForegroundColor Cyan

python awesome_api_server.py $Port
