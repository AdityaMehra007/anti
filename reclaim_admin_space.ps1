# Ensure Running with Admin Privileges
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Elevating privileges to Administrator..." -ForegroundColor Yellow
    Start-Process powershell.exe -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "   ANTIGRAVITY OMEGA - ELEVATED C: DRIVE SPACE MAXIMIZER" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan

$cBefore = (Get-PSDrive C).Free / 1GB
Write-Host ("Initial C: Free Space: {0:N2} GB" -f $cBefore) -ForegroundColor Green

# 1. Remove obsolete leftover directories
Write-Host "`n[1/6] Removing obsolete program folders and reset logs..." -ForegroundColor Yellow
$obsolete = @("C:\Program Files\LGHUB.old", "C:\$SysReset", "C:\OneDriveTemp", "C:\tmp")
foreach ($dir in $obsolete) {
    if (Test-Path $dir) {
        Remove-Item -Path $dir -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  Removed: $dir" -ForegroundColor Gray
    }
}

# 2. Stop update services and purge Windows Update Download cache (reclaims ~900 MB)
Write-Host "`n[2/6] Purging Windows Update Download Cache (900 MB)..." -ForegroundColor Yellow
Stop-Service -Name wuauserv -Force -ErrorAction SilentlyContinue
Stop-Service -Name bits -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\Windows\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue
Start-Service -Name bits -ErrorAction SilentlyContinue
Start-Service -Name wuauserv -ErrorAction SilentlyContinue
Write-Host "  Purged SoftwareDistribution\Download." -ForegroundColor Gray

# 3. Clean Delivery Optimization cache
Write-Host "`n[3/6] Purging Delivery Optimization Cache..." -ForegroundColor Yellow
Remove-Item -Path "C:\Windows\SoftwareDistribution\DeliveryOptimization\*" -Recurse -Force -ErrorAction SilentlyContinue
Delete-DeliveryOptimizationCache -ErrorAction SilentlyContinue

# 4. Clean System Crash Dumps and Error Reports
Write-Host "`n[4/6] Purging Windows Error Reporting and Crash Dumps..." -ForegroundColor Yellow
Remove-Item -Path "C:\Windows\Minidump\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\Windows\Memory.dmp" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\ProgramData\Microsoft\Windows\WER\ReportArchive\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\ProgramData\Microsoft\Windows\WER\ReportQueue\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue

# 5. Dism Component Store Cleanup (reclaims 2 to 5 GB from WinSxS)
Write-Host "`n[5/6] Running DISM Component Store Cleanup (/ResetBase)..." -ForegroundColor Yellow
Write-Host "  (This may take 3-5 minutes, compressing and removing superseded updates)" -ForegroundColor Gray
Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase

# 6. Recycle Bin
Write-Host "`n[6/6] Emptying Recycle Bin..." -ForegroundColor Yellow
Clear-RecycleBin -DriveLetter C -Force -ErrorAction SilentlyContinue

$cAfter = (Get-PSDrive C).Free / 1GB
$gained = $cAfter - $cBefore
Write-Host "`n=====================================================================" -ForegroundColor Cyan
Write-Host ("ELEVATED CLEANUP COMPLETE! Final C: Free Space: {0:N2} GB (+{1:N2} GB Reclaimed)" -f $cAfter, $gained) -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
