<#
.SYNOPSIS
    Supabase Autonomous Control & Local Stack Manager
.DESCRIPTION
    Checks Docker daemon status, manages environment files, launches or stops
    the Supabase microservices stack, and prints service URLs.
#>

param (
    [Parameter(Mandatory=$false)]
    [ValidateSet('up', 'down', 'restart', 'status', 'logs')]
    [string]$Action = 'up'
)

$Host.UI.RawUI.WindowTitle = "Supabase Local Stack Manager"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SupabaseDir = Join-Path $ScriptDir "supabase"
$EnvFile = Join-Path $SupabaseDir ".env"
$EnvDocker = Join-Path $SupabaseDir ".env.docker"

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "       SUPABASE AUTONOMOUS CONTROL & MANAGER       " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Environment file check
if (-not (Test-Path $EnvFile)) {
    if (Test-Path $EnvDocker) {
        Write-Host "[*] Initializing supabase/.env from .env.docker..." -ForegroundColor Yellow
        Copy-Item $EnvDocker $EnvFile
    } else {
        Write-Host "[-] Missing .env.docker configuration template." -ForegroundColor Red
    }
}

# 2. Check Docker daemon availability
Write-Host "[*] Checking Docker status..." -ForegroundColor Gray
$dockerCheck = & docker ps 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[!] Docker daemon is not running." -ForegroundColor Red
    Write-Host "    To run the local Supabase containers:" -ForegroundColor Yellow
    Write-Host "    1. Start Docker Desktop from the Start menu." -ForegroundColor White
    Write-Host "    2. Wait for Docker engine to initialize." -ForegroundColor White
    Write-Host "    3. Re-run this launcher." -ForegroundColor White
    Write-Host ""
    Write-Host "    Alternatively, you can connect the clients to Supabase Cloud by setting:" -ForegroundColor Green
    Write-Host "    SUPABASE_URL=https://<your-project>.supabase.co" -ForegroundColor Green
    Write-Host "    SUPABASE_ANON_KEY=<your-anon-key>" -ForegroundColor Green
    Write-Host ""
    Write-Host "    Opening SUPABASE_CONTROL_CENTER.html for diagnostics..." -ForegroundColor Cyan
    Start-Process (Join-Path $ScriptDir "SUPABASE_CONTROL_CENTER.html")
    exit 0
}

# 3. Process commands
Push-Location $SupabaseDir
try {
    switch ($Action) {
        'up' {
            Write-Host "[+] Launching Supabase local services (docker compose up -d)..." -ForegroundColor Green
            & docker compose --env-file $EnvFile up -d
            if ($LASTEXITCODE -eq 0) {
                Write-Host ""
                Write-Host "===================================================" -ForegroundColor Cyan
                Write-Host "       SUPABASE SERVICES ONLINE & READY           " -ForegroundColor Cyan
                Write-Host "===================================================" -ForegroundColor Cyan
                Write-Host "  * Studio UI:     http://localhost:3000" -ForegroundColor Yellow
                Write-Host "  * Kong Gateway:  http://localhost:8000" -ForegroundColor White
                Write-Host "  * REST API:      http://localhost:8000/rest/v1" -ForegroundColor White
                Write-Host "  * Auth API:      http://localhost:8000/auth/v1" -ForegroundColor White
                Write-Host "  * Storage API:   http://localhost:8000/storage/v1" -ForegroundColor White
                Write-Host "  * Postgres DB:   localhost:5432 (user: postgres, pass: postgres)" -ForegroundColor Gray
                Write-Host "===================================================" -ForegroundColor Cyan
                Write-Host ""
                Write-Host "[*] Launching Control Center..." -ForegroundColor Cyan
                Start-Process (Join-Path $ScriptDir "SUPABASE_CONTROL_CENTER.html")
            }
        }
        'down' {
            Write-Host "[*] Stopping Supabase services..." -ForegroundColor Yellow
            & docker compose --env-file $EnvFile down
        }
        'restart' {
            Write-Host "[*] Restarting Supabase services..." -ForegroundColor Yellow
            & docker compose --env-file $EnvFile restart
        }
        'status' {
            & docker compose --env-file $EnvFile ps
        }
        'logs' {
            & docker compose --env-file $EnvFile logs -f --tail 100
        }
    }
} finally {
    Pop-Location
}
