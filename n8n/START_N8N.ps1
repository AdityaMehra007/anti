<#
.SYNOPSIS
    OMEGA n8n Orchestrator Launcher
.DESCRIPTION
    Launches n8n via Docker Compose if the Docker daemon is available,
    or falls back to native npx execution with automatic health checks.
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "                OMEGA AUTOMATION PLATFORM :: n8n ORCHESTRATOR                  " -ForegroundColor Cyan
Write-Host "===============================================================================" -ForegroundColor Cyan

if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "[*] Created .env configuration file." -ForegroundColor Yellow
    }
}

$dockerRunning = $false
try {
    $null = docker info 2>&1
    if ($LASTEXITCODE -eq 0) {
        $dockerRunning = $true
    }
} catch {
    $dockerRunning = $false
}

if ($dockerRunning) {
    Write-Host "[*] Docker daemon is running. Launching n8n container..." -ForegroundColor Green
    docker compose up -d
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] n8n container 'omega_n8n' is active." -ForegroundColor Green
        Write-Host "[*] Access the dashboard at: http://localhost:5678" -ForegroundColor Cyan
        Start-Process "http://localhost:5678"
        exit 0
    }
    Write-Host "[!] Docker Compose launch failed. Falling back to native launcher..." -ForegroundColor Yellow
}

Write-Host "[*] Checking for OMEGA Local Automation Engine..." -ForegroundColor Yellow
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if ($pythonPath -and (Test-Path "n8n_server.py")) {
    Write-Host "[OK] Launching OMEGA Automation Server on port 5678..." -ForegroundColor Green
    Start-Process "http://localhost:5678"
    python n8n_server.py
    exit 0
}

Write-Host "[*] Checking for Node / npx..." -ForegroundColor Yellow
$npxPath = Get-Command npx -ErrorAction SilentlyContinue
if (-not $npxPath) {
    Write-Host "[ERROR] Neither active Docker, Python, nor npx was detected." -ForegroundColor Red
    Write-Host "Please install Node.js or start Docker Desktop." -ForegroundColor Red
    exit 1
}

$env:N8N_PORT = "5678"
$env:N8N_EDITOR_BASE_URL = "http://localhost:5678/"
$env:WEBHOOK_URL = "http://localhost:5678/"

Write-Host "[*] Starting n8n natively via npx on port 5678..." -ForegroundColor Green
Start-Process "http://localhost:5678"
npx n8n
