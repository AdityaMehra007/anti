# MASTER LAUNCHER: Run all waves sequentially
# Usage: powershell -ExecutionPolicy Bypass -File launch_all_waves.ps1

param(
    [ValidateSet("all","1","2","3","4")]
    [string]$Wave = "all"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

function Run-Wave {
    param([string]$WaveNum, [string]$Script, [string]$Desc)
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Magenta
    Write-Host "  WAVE $WaveNum: $Desc" -ForegroundColor Magenta
    Write-Host "============================================" -ForegroundColor Magenta
    Write-Host ""
    
    $response = Read-Host "Launch Wave $WaveNum? (y/n)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        & "$scriptDir\$Script"
        Write-Host ""
        Write-Host "Wave $WaveNum complete. Apply to all open tabs before continuing." -ForegroundColor Yellow
        Read-Host "Press Enter when done with Wave $WaveNum"
    } else {
        Write-Host "Skipped Wave $WaveNum." -ForegroundColor DarkGray
    }
}

Write-Host @"
  ___  __  __ ___ ___   _     _   _   _ _  _  ___ _  _ 
 / _ \|  \/  | __/ __| /_\   | | /_\ | | || |/ _ | || |
| (_) | |\/| | _| (_ |/ _ \  | |/ _ \| |_|| | (_) | __ |
 \___/|_|  |_|___\___/_/ \_\ |_/_/ \_\___/|_|\___/|_||_|

  MASTER APPLICATION DISPATCH — Aditya Mehra
  Total: 151 direct job applications across 4 waves
"@ -ForegroundColor Cyan

if ($Wave -eq "all" -or $Wave -eq "1") {
    Run-Wave "1" "open_all_jobs_wave1_linkedin.ps1" "40 LinkedIn Quick Apply Jobs"
}
if ($Wave -eq "all" -or $Wave -eq "2") {
    Run-Wave "2" "open_all_jobs_wave2_indeed.ps1" "39 Indeed Job Listings"
}
if ($Wave -eq "all" -or $Wave -eq "3") {
    Run-Wave "3" "open_all_jobs_wave3_ats.ps1" "37 ATS/Workday Portal Submissions"
}
if ($Wave -eq "all" -or $Wave -eq "4") {
    Run-Wave "4" "open_all_jobs_wave4_remote.ps1" "35 Remote-First Career Pages"
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  ALL WAVES COMPLETE!" -ForegroundColor Green
Write-Host "  Total applications dispatched: 151" -ForegroundColor Green
Write-Host "  + 254 existing packages already prepared" -ForegroundColor Green
Write-Host "  = 405+ companies in your pipeline" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
