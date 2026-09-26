<#
.SYNOPSIS
    freeCodeCamp Autonomous Control & Local Stack Manager
.DESCRIPTION
    Manages MongoDB replica set, Mailpit, dependency installation, seeding,
    and running the Fastify API and Gatsby client.
#>

param (
    [Parameter(Mandatory=$false)]
    [ValidateSet('dev', 'db-up', 'db-down', 'seed', 'install', 'status')]
    [string]$Action = 'dev'
)

$Host.UI.RawUI.WindowTitle = "freeCodeCamp Local Stack Manager"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$FccDir = Join-Path $ScriptDir "external\freeCodeCamp"
$EnvFile = Join-Path $FccDir ".env"
$SampleEnv = Join-Path $FccDir "sample.env"

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "     freeCodeCamp AUTONOMOUS STACK MANAGER        " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $FccDir)) {
    Write-Host "[-] freeCodeCamp repository not found at: $FccDir" -ForegroundColor Red
    exit 1
}

# 1. Environment file check
if (-not (Test-Path $EnvFile)) {
    if (Test-Path $SampleEnv) {
        Write-Host "[*] Creating .env from sample.env..." -ForegroundColor Yellow
        Copy-Item $SampleEnv $EnvFile
    }
}

# 2. Check Docker daemon availability
Write-Host "[*] Checking Docker status..." -ForegroundColor Gray
$dockerCheck = & docker ps 2>&1
$DockerAvailable = ($LASTEXITCODE -eq 0)

if (-not $DockerAvailable) {
    Write-Host "[!] Docker daemon is not active. Please launch Docker Desktop." -ForegroundColor Yellow
}

Push-Location $FccDir
try {
    switch ($Action) {
        'db-up' {
            if (-not $DockerAvailable) {
                Write-Host "[-] Docker is required to launch MongoDB replica set." -ForegroundColor Red
                break
            }
            Write-Host "[+] Starting MongoDB (rs0) and Mailpit..." -ForegroundColor Green
            & docker compose -f docker/docker-compose.yml -f docker/docker-compose.ports.yml up -d
        }
        'db-down' {
            Write-Host "[*] Stopping MongoDB and Mailpit containers..." -ForegroundColor Yellow
            & docker compose -f docker/docker-compose.yml -f docker/docker-compose.ports.yml down
        }
        'install' {
            Write-Host "[+] Running pnpm install..." -ForegroundColor Green
            & pnpm install
        }
        'seed' {
            Write-Host "[+] Preseeding & seeding demo user..." -ForegroundColor Green
            & pnpm run preseed
            & pnpm run seed
        }
        'status' {
            Write-Host "[*] Service Status Check:" -ForegroundColor Cyan
            & docker compose -f docker/docker-compose.yml ps
        }
        'dev' {
            if ($DockerAvailable) {
                Write-Host "[1/3] Ensuring Database (MongoDB rs0) is running..." -ForegroundColor Cyan
                & docker compose -f docker/docker-compose.yml -f docker/docker-compose.ports.yml up -d
            } else {
                Write-Host "[!] Docker not detected; skipping container auto-start." -ForegroundColor Yellow
            }
            Write-Host "[2/3] Local endpoints configured:" -ForegroundColor Cyan
            Write-Host "      - Client: http://localhost:8000" -ForegroundColor White
            Write-Host "      - API:    http://localhost:3000" -ForegroundColor White
            Write-Host "      - Docs:   http://localhost:3000/documentation" -ForegroundColor White
            Write-Host "      - Mail:   http://localhost:8025" -ForegroundColor White
            Write-Host "[3/3] Starting development servers (turbo develop)..." -ForegroundColor Green
            & pnpm run develop
        }
    }
} finally {
    Pop-Location
}
