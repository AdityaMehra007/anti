<#
.SYNOPSIS
    Starts the Apache Airflow Autonomous API Server & Mission Control Cockpit on Windows.
.PARAMETER Port
    HTTP port to bind (default: 8775).
.PARAMETER Docker
    Switch to start the multi-container Docker Compose stack instead of local mock daemon.
#>
param(
    [int]$Port = 8775,
    [switch]$Docker
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir
Set-Location $RootDir

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  OMEGA APACHE AIRFLOW ORCHESTRATION LAUNCHER (WINDOWS Core/7+)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

if ($Docker) {
    Write-Host "[*] Launching Airflow Production Celery/Postgres/Redis Docker Stack..." -ForegroundColor Yellow
    Set-Location "$RootDir\stacks\airflow"
    docker compose up -d
    Write-Host "[+] Docker stack online! Webserver listening on http://localhost:8080" -ForegroundColor Green
    Start-Process "http://localhost:8080"
    exit 0
}

Write-Host "[*] Launching Airflow Autonomous API Server on port $Port..." -ForegroundColor Green
Start-Process "http://localhost:$Port/cockpit"
python "$RootDir\airflow_api_server.py" --port $Port
