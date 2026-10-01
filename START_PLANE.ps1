<#
.SYNOPSIS
    Plane Community Edition (CE) Local Stack Manager & Autonomous Controller
.DESCRIPTION
    Manages Docker daemon discovery, environment variables, lifecycle operations (up, down, restart, status, logs),
    and opens the Plane web interface at http://localhost:8090.
#>

param (
    [Parameter(Mandatory=$false)]
    [ValidateSet('up', 'down', 'restart', 'status', 'logs', 'browser', 'sync')]
    [string]$Action = 'up'
)

$Host.UI.RawUI.WindowTitle = "Plane CE Local Stack Controller"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PlaneDir = Join-Path $ScriptDir "external\plane"
$EnvFile = Join-Path $PlaneDir "plane.env"
$EnvExample = Join-Path $PlaneDir "plane.env.example"
$ComposeFile = Join-Path $PlaneDir "docker-compose.yaml"
$WebUrl = "http://localhost:8090"
$DockerDesktopPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "             PLANE COMMUNITY EDITION (CE) - AUTONOMOUS CONTROL                " -ForegroundColor Cyan
Write-Host "             Target Web Ingress: $WebUrl                              " -ForegroundColor DarkCyan
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Environment Verification
if (-not (Test-Path $EnvFile)) {
    if (Test-Path $EnvExample) {
        Write-Host "[*] Initializing plane.env from plane.env.example..." -ForegroundColor Yellow
        Copy-Item $EnvExample $EnvFile
    } else {
        Write-Host "[-] Missing plane.env.example template." -ForegroundColor Red
        exit 1
    }
}

# 2. Docker Daemon Verification & Auto-Discovery
function Test-DockerDaemon {
    $null = & docker ps 2>&1
    return ($LASTEXITCODE -eq 0)
}

Write-Host "[*] Checking Docker daemon status..." -ForegroundColor Gray
$isDockerRunning = Test-DockerDaemon

if (-not $isDockerRunning) {
    Write-Host "[!] Docker daemon is not active." -ForegroundColor Yellow
    if ($Action -eq 'up' -or $Action -eq 'restart') {
        if (Test-Path $DockerDesktopPath) {
            Write-Host "[+] Launching Docker Desktop engine from $DockerDesktopPath..." -ForegroundColor Green
            Start-Process $DockerDesktopPath
            Write-Host "[*] Waiting for Docker daemon to initialize (up to 60s)..." -ForegroundColor Gray
            $waited = 0
            while ($waited -lt 60) {
                Start-Sleep -Seconds 3
                $waited += 3
                Write-Host "    ...checking engine ($waited s)" -ForegroundColor DarkGray
                if (Test-DockerDaemon) {
                    $isDockerRunning = $true
                    Write-Host "[+] Docker daemon successfully connected!" -ForegroundColor Green
                    break
                }
            }
        }
    }
    
    if (-not $isDockerRunning) {
        Write-Host ""
        Write-Host "[!] Docker daemon is still unavailable." -ForegroundColor Red
        Write-Host "    To start Plane CE locally:" -ForegroundColor Yellow
        Write-Host "    1. Start Docker Desktop manually from the Start Menu." -ForegroundColor White
        Write-Host "    2. Wait until the whale icon in system tray turns steady green." -ForegroundColor White
        Write-Host "    3. Re-run START_PLANE.bat" -ForegroundColor White
        Write-Host ""
        Write-Host "    Note: You can still run offline API simulations via:" -ForegroundColor Cyan
        Write-Host "    python omega/integrations/plane_connector.py --dry-run --status" -ForegroundColor Cyan
        exit 1
    }
}

# 3. Lifecycle Commands Execution
Push-Location $PlaneDir
try {
    switch ($Action) {
        'up' {
            Write-Host "[*] Starting Plane CE microservices stack (detached)..." -ForegroundColor Green
            & docker compose -f $ComposeFile --env-file $EnvFile up -d
            if ($LASTEXITCODE -eq 0) {
                Write-Host ""
                Write-Host "[+] Plane stack launched successfully!" -ForegroundColor Green
                Write-Host "    Services: Web, API, Space, Admin, Live, PostgreSQL, Redis, RabbitMQ, MinIO" -ForegroundColor Gray
                Write-Host "    URL: $WebUrl" -ForegroundColor Cyan
                Write-Host ""
                Write-Host "[*] Waiting for web ingress gateway..." -ForegroundColor Yellow
                Start-Sleep -Seconds 5
                Start-Process $WebUrl
            } else {
                Write-Host "[-] Failed to launch Plane containers. Review errors above." -ForegroundColor Red
            }
        }

        'down' {
            Write-Host "[*] Stopping Plane CE stack..." -ForegroundColor Yellow
            & docker compose -f $ComposeFile --env-file $EnvFile down
            Write-Host "[+] Stack stopped safely." -ForegroundColor Green
        }

        'restart' {
            Write-Host "[*] Restarting Plane stack..." -ForegroundColor Yellow
            & docker compose -f $ComposeFile --env-file $EnvFile restart
            Write-Host "[+] Restart complete." -ForegroundColor Green
        }

        'status' {
            Write-Host "[*] Container Status:" -ForegroundColor Cyan
            & docker compose -f $ComposeFile --env-file $EnvFile ps
            Write-Host ""
            Write-Host "[*] Testing API Health probe ($WebUrl/api/instances/)..." -ForegroundColor Gray
            try {
                $response = Invoke-WebRequest -Uri "$WebUrl/api/instances/" -Method Get -TimeoutSec 3 -ErrorAction Stop
                Write-Host "[+] Instance API reachable (Status $($response.StatusCode))" -ForegroundColor Green
            } catch {
                Write-Host "[-] Instance API not responding yet or stack initializing." -ForegroundColor Yellow
            }
        }

        'logs' {
            Write-Host "[*] Streaming container logs (Ctrl+C to exit)..." -ForegroundColor Cyan
            & docker compose -f $ComposeFile --env-file $EnvFile logs -f --tail=100
        }

        'browser' {
            Write-Host "[*] Opening Plane Web Dashboard: $WebUrl..." -ForegroundColor Cyan
            Start-Process $WebUrl
        }

        'sync' {
            Write-Host "[*] Executing OMEGA Agent Task Synchronization..." -ForegroundColor Cyan
            Pop-Location
            & python omega/orchestration/plane_dispatcher.py --sync
            return
        }
    }
}
finally {
    Pop-Location
}
