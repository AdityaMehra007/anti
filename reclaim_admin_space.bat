@echo off
setlocal enabledelayedexpansion

:: =====================================================================
::    ANTIGRAVITY OMEGA - ULTIMATE C: DRIVE MAX SPACE RECLAIMER (ADMIN)
:: =====================================================================

:: Check for Admin Privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] This script must be run as Administrator!
    echo Please right-click this file and choose 'Run as administrator',
    echo or double-click the RECLAIM_ADMIN_C_DRIVE shortcut on your Desktop.
    echo.
    pause
    exit /b 1
)

set LOGFILE=E:\anti\reclaim_admin_space.log
echo [START] Admin Reclaim started at %date% %time% > "%LOGFILE%"

echo =====================================================================
echo    ANTIGRAVITY OMEGA - ULTIMATE C: DRIVE MAX SPACE RECLAIMER
echo =====================================================================
echo Target: Reclaiming 20+ GB of system, app and cache bloat to E: drive.
echo Log file: %LOGFILE%
echo.

:: ---------------------------------------------------------------------
:: 1. STOPPING BACKGROUND SERVICES & PROCESSES
:: ---------------------------------------------------------------------
echo [1/18] Stopping conflicting background services and processes...
echo Stopping background services... >> "%LOGFILE%"

net stop "ClickToRunSvc" >nul 2>&1
net stop "wslservice" >nul 2>&1
net stop "Lenovo Vantage Service" >nul 2>&1
net stop "ImControllerService" >nul 2>&1
net stop "wuauserv" >nul 2>&1
net stop "bits" >nul 2>&1

taskkill /F /IM lghub_agent.exe /IM lghub_system_tray.exe /IM lghub_updater.exe /IM lghub.exe >nul 2>&1
taskkill /F /IM SteelSeriesGG.exe /IM SteelSeriesGGClient.exe /IM SteelSeriesEngine.exe >nul 2>&1
taskkill /F /IM EpicGamesLauncher.exe /IM EpicWebHelper.exe /IM EpicOnlineServicesUserHelper.exe /IM EpicOnlineServicesUIHelper.exe /IM EOSOverlayRenderer-Win64-Shipping.exe >nul 2>&1
taskkill /F /IM EADesktop.exe /IM EABackgroundService.exe /IM Link2EA.exe >nul 2>&1
taskkill /F /IM msedge.exe /IM msedgewebview2.exe >nul 2>&1
timeout /t 2 /nobreak >nul
echo   Done.

:: ---------------------------------------------------------------------
:: 2. REMOVING OBSOLETE LGHUB BACKUP (203 MB)
:: ---------------------------------------------------------------------
echo [2/18] Removing obsolete LGHUB update backups (203 MB)...
if exist "C:\Program Files\LGHUB.old" (
    rmdir /s /q "C:\Program Files\LGHUB.old" >> "%LOGFILE%" 2>&1
    echo   Removed C:\Program Files\LGHUB.old.
)

:: ---------------------------------------------------------------------
:: 3. PURGING OBSOLETE EDGE & EDGECORE OLD BUILDS (3+ GB)
:: ---------------------------------------------------------------------
echo [3/18] Purging superseded Microsoft Edge, EdgeCore and WebView builds (3+ GB)...
if exist "C:\Program Files (x86)\Microsoft\EdgeCore\153.0.4234.48" (
    rmdir /s /q "C:\Program Files (x86)\Microsoft\EdgeCore\153.0.4234.48" >> "%LOGFILE%" 2>&1
    echo   Purged EdgeCore 153.0.4234.48 (699 MB).
)
if exist "C:\Program Files (x86)\Microsoft\EdgeCore\154.0.4258.37" (
    rmdir /s /q "C:\Program Files (x86)\Microsoft\EdgeCore\154.0.4258.37" >> "%LOGFILE%" 2>&1
    echo   Purged EdgeCore 154.0.4258.37 (700 MB).
)
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\153.0.4234.48" (
    rmdir /s /q "C:\Program Files (x86)\Microsoft\Edge\Application\153.0.4234.48" >> "%LOGFILE%" 2>&1
    echo   Purged Edge Application 153.0.4234.48 (872 MB).
)
if exist "C:\Program Files (x86)\Microsoft\EdgeWebView\Application\154.0.4258.37" (
    rmdir /s /q "C:\Program Files (x86)\Microsoft\EdgeWebView\Application\154.0.4258.37" >> "%LOGFILE%" 2>&1
    echo   Purged EdgeWebView 154.0.4258.37 (861 MB).
)

:: ---------------------------------------------------------------------
:: 4. PURGING GOOGLE UPDATER CRX CACHE (518 MB)
:: ---------------------------------------------------------------------
echo [4/18] Purging Google Updater CRX extension cache (518 MB)...
if exist "C:\Program Files (x86)\Google\GoogleUpdater\crx_cache" (
    rmdir /s /q "C:\Program Files (x86)\Google\GoogleUpdater\crx_cache" >> "%LOGFILE%" 2>&1
    echo   Purged Google CRX Cache.
)

:: ---------------------------------------------------------------------
:: 5. MIGRATING MICROSOFT OFFICE (3.88 GB)
:: ---------------------------------------------------------------------
echo [5/18] Migrating Microsoft Office (3.88 GB) to E: drive...
if exist "C:\Program Files (x86)\Microsoft Office" (
    mkdir "E:\anti gravity\Program Files (x86)\Microsoft Office" 2>nul
    robocopy "C:\Program Files (x86)\Microsoft Office" "E:\anti gravity\Program Files (x86)\Microsoft Office" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\Program Files (x86)\Microsoft Office" 2>nul
    mklink /J "C:\Program Files (x86)\Microsoft Office" "E:\anti gravity\Program Files (x86)\Microsoft Office" >> "%LOGFILE%" 2>&1
    echo   Junction created for Microsoft Office.
)

:: ---------------------------------------------------------------------
:: 6. MIGRATING LGHUB DEPOTS & CACHE (1.22 GB)
:: ---------------------------------------------------------------------
echo [6/18] Migrating LGHUB Depots & Cache (1.22 GB) to E: drive...
if exist "C:\ProgramData\LGHUB\depots" (
    mkdir "E:\anti gravity\ProgramData\LGHUB\depots" 2>nul
    robocopy "C:\ProgramData\LGHUB\depots" "E:\anti gravity\ProgramData\LGHUB\depots" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\ProgramData\LGHUB\depots" 2>nul
    mklink /J "C:\ProgramData\LGHUB\depots" "E:\anti gravity\ProgramData\LGHUB\depots" >> "%LOGFILE%" 2>&1
    echo   Junction created for LGHUB depots.
)
if exist "C:\ProgramData\LGHUB\cache" (
    mkdir "E:\anti gravity\ProgramData\LGHUB\cache" 2>nul
    robocopy "C:\ProgramData\LGHUB\cache" "E:\anti gravity\ProgramData\LGHUB\cache" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\ProgramData\LGHUB\cache" 2>nul
    mklink /J "C:\ProgramData\LGHUB\cache" "E:\anti gravity\ProgramData\LGHUB\cache" >> "%LOGFILE%" 2>&1
    echo   Junction created for LGHUB cache.
)

:: ---------------------------------------------------------------------
:: 7. MIGRATING LGHUB PROGRAM FILES (574 MB)
:: ---------------------------------------------------------------------
echo [7/18] Migrating LGHUB Application (574 MB) to E: drive...
if exist "C:\Program Files\LGHUB" (
    mkdir "E:\anti gravity\Program Files\LGHUB" 2>nul
    robocopy "C:\Program Files\LGHUB" "E:\anti gravity\Program Files\LGHUB" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\Program Files\LGHUB" 2>nul
    mklink /J "C:\Program Files\LGHUB" "E:\anti gravity\Program Files\LGHUB" >> "%LOGFILE%" 2>&1
    echo   Junction created for LGHUB Application.
)

:: ---------------------------------------------------------------------
:: 8. MIGRATING STEELSERIES GG (1.36 GB)
:: ---------------------------------------------------------------------
echo [8/18] Migrating SteelSeries GG (1.36 GB) to E: drive...
if exist "C:\Program Files\SteelSeries\GG" (
    mkdir "E:\anti gravity\Program Files\SteelSeries\GG" 2>nul
    robocopy "C:\Program Files\SteelSeries\GG" "E:\anti gravity\Program Files\SteelSeries\GG" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\Program Files\SteelSeries\GG" 2>nul
    mklink /J "C:\Program Files\SteelSeries\GG" "E:\anti gravity\Program Files\SteelSeries\GG" >> "%LOGFILE%" 2>&1
    echo   Junction created for SteelSeries GG.
)

:: ---------------------------------------------------------------------
:: 9. MIGRATING EPIC ONLINE SERVICES (1.13 GB)
:: ---------------------------------------------------------------------
echo [9/18] Migrating Epic Online Services (1.13 GB) to E: drive...
if exist "C:\Program Files (x86)\Epic Games\Epic Online Services" (
    mkdir "E:\anti gravity\Program Files (x86)\Epic Games\Epic Online Services" 2>nul
    robocopy "C:\Program Files (x86)\Epic Games\Epic Online Services" "E:\anti gravity\Program Files (x86)\Epic Games\Epic Online Services" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\Program Files (x86)\Epic Games\Epic Online Services" 2>nul
    mklink /J "C:\Program Files (x86)\Epic Games\Epic Online Services" "E:\anti gravity\Program Files (x86)\Epic Games\Epic Online Services" >> "%LOGFILE%" 2>&1
    echo   Junction created for Epic Online Services.
)

:: ---------------------------------------------------------------------
:: 10. MIGRATING ELECTRONIC ARTS EA DESKTOP (530 MB)
:: ---------------------------------------------------------------------
echo [10/18] Migrating EA Desktop (530 MB) to E: drive...
if exist "C:\Program Files\Electronic Arts\EA Desktop" (
    mkdir "E:\anti gravity\Program Files\Electronic Arts\EA Desktop" 2>nul
    robocopy "C:\Program Files\Electronic Arts\EA Desktop" "E:\anti gravity\Program Files\Electronic Arts\EA Desktop" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\Program Files\Electronic Arts\EA Desktop" 2>nul
    mklink /J "C:\Program Files\Electronic Arts\EA Desktop" "E:\anti gravity\Program Files\Electronic Arts\EA Desktop" >> "%LOGFILE%" 2>&1
    echo   Junction created for EA Desktop.
)

:: ---------------------------------------------------------------------
:: 11. MIGRATING LENOVO VANTAGE & APP SUITE (1.80 GB)
:: ---------------------------------------------------------------------
echo [11/18] Migrating Lenovo Vantage & App Suite (1.80 GB) to E: drive...
if exist "C:\ProgramData\Lenovo\Vantage" (
    mkdir "E:\anti gravity\ProgramData\Lenovo\Vantage" 2>nul
    robocopy "C:\ProgramData\Lenovo\Vantage" "E:\anti gravity\ProgramData\Lenovo\Vantage" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\ProgramData\Lenovo\Vantage" 2>nul
    mklink /J "C:\ProgramData\Lenovo\Vantage" "E:\anti gravity\ProgramData\Lenovo\Vantage" >> "%LOGFILE%" 2>&1
    echo   Junction created for Lenovo Vantage Data.
)
if exist "C:\ProgramData\Lenovo\ImController" (
    mkdir "E:\anti gravity\ProgramData\Lenovo\ImController" 2>nul
    robocopy "C:\ProgramData\Lenovo\ImController" "E:\anti gravity\ProgramData\Lenovo\ImController" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\ProgramData\Lenovo\ImController" 2>nul
    mklink /J "C:\ProgramData\Lenovo\ImController" "E:\anti gravity\ProgramData\Lenovo\ImController" >> "%LOGFILE%" 2>&1
    echo   Junction created for Lenovo ImController Data.
)
if exist "C:\Program Files (x86)\Lenovo\Legion Arena" (
    mkdir "E:\anti gravity\Program Files (x86)\Lenovo\Legion Arena" 2>nul
    robocopy "C:\Program Files (x86)\Lenovo\Legion Arena" "E:\anti gravity\Program Files (x86)\Lenovo\Legion Arena" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\Program Files (x86)\Lenovo\Legion Arena" 2>nul
    mklink /J "C:\Program Files (x86)\Lenovo\Legion Arena" "E:\anti gravity\Program Files (x86)\Lenovo\Legion Arena" >> "%LOGFILE%" 2>&1
    echo   Junction created for Legion Arena.
)
if exist "C:\Program Files (x86)\Lenovo\LenovoNow" (
    mkdir "E:\anti gravity\Program Files (x86)\Lenovo\LenovoNow" 2>nul
    robocopy "C:\Program Files (x86)\Lenovo\LenovoNow" "E:\anti gravity\Program Files (x86)\Lenovo\LenovoNow" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\Program Files (x86)\Lenovo\LenovoNow" 2>nul
    mklink /J "C:\Program Files (x86)\Lenovo\LenovoNow" "E:\anti gravity\Program Files (x86)\Lenovo\LenovoNow" >> "%LOGFILE%" 2>&1
    echo   Junction created for LenovoNow.
)

:: ---------------------------------------------------------------------
:: 12. MIGRATING PACKAGE CACHE (647 MB)
:: ---------------------------------------------------------------------
echo [12/18] Migrating Windows Installer Package Cache (647 MB) to E: drive...
if exist "C:\ProgramData\Package Cache" (
    mkdir "E:\anti gravity\ProgramData\Package Cache" 2>nul
    robocopy "C:\ProgramData\Package Cache" "E:\anti gravity\ProgramData\Package Cache" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\ProgramData\Package Cache" 2>nul
    mklink /J "C:\ProgramData\Package Cache" "E:\anti gravity\ProgramData\Package Cache" >> "%LOGFILE%" 2>&1
    echo   Junction created for Package Cache.
)

:: ---------------------------------------------------------------------
:: 13. MIGRATING WSL (828 MB)
:: ---------------------------------------------------------------------
echo [13/18] Migrating Windows Subsystem for Linux (828 MB) to E: drive...
if exist "C:\Program Files\WSL" (
    mkdir "E:\anti gravity\Program Files\WSL" 2>nul
    robocopy "C:\Program Files\WSL" "E:\anti gravity\Program Files\WSL" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\Program Files\WSL" 2>nul
    mklink /J "C:\Program Files\WSL" "E:\anti gravity\Program Files\WSL" >> "%LOGFILE%" 2>&1
    echo   Junction created for WSL.
)

:: ---------------------------------------------------------------------
:: 14. MIGRATING NVIDIA APP & INSTALLER2 (834 MB)
:: ---------------------------------------------------------------------
echo [14/18] Migrating NVIDIA App & Installer2 (834 MB) to E: drive...
if exist "C:\Program Files\NVIDIA Corporation\Installer2" (
    mkdir "E:\anti gravity\Program Files\NVIDIA Corporation\Installer2" 2>nul
    robocopy "C:\Program Files\NVIDIA Corporation\Installer2" "E:\anti gravity\Program Files\NVIDIA Corporation\Installer2" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\Program Files\NVIDIA Corporation\Installer2" 2>nul
    mklink /J "C:\Program Files\NVIDIA Corporation\Installer2" "E:\anti gravity\Program Files\NVIDIA Corporation\Installer2" >> "%LOGFILE%" 2>&1
    echo   Junction created for NVIDIA Installer2.
)
if exist "C:\Program Files\NVIDIA Corporation\NVIDIA app" (
    mkdir "E:\anti gravity\Program Files\NVIDIA Corporation\NVIDIA app" 2>nul
    robocopy "C:\Program Files\NVIDIA Corporation\NVIDIA app" "E:\anti gravity\Program Files\NVIDIA Corporation\NVIDIA app" /E /MOVE /R:1 /W:1 /NP /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1
    rmdir /s /q "C:\Program Files\NVIDIA Corporation\NVIDIA app" 2>nul
    mklink /J "C:\Program Files\NVIDIA Corporation\NVIDIA app" "E:\anti gravity\Program Files\NVIDIA Corporation\NVIDIA app" >> "%LOGFILE%" 2>&1
    echo   Junction created for NVIDIA app.
)

:: ---------------------------------------------------------------------
:: 15. PURGING WINDOWS UPDATE DOWNLOAD CACHE (900 MB)
:: ---------------------------------------------------------------------
echo [15/18] Purging Windows Update Download Cache (900 MB)...
del /q /s /f "C:\Windows\SoftwareDistribution\Download\*" >> "%LOGFILE%" 2>&1
for /d %%p in ("C:\Windows\SoftwareDistribution\Download\*") do rmdir /s /q "%%p" >> "%LOGFILE%" 2>&1
echo   Done.

:: ---------------------------------------------------------------------
:: 16. RUNNING DISM COMPONENT STORE CLEANUP (3 TO 5 GB RECLAIM)
:: ---------------------------------------------------------------------
echo [16/18] Cleaning superseded Windows components (WinSxS /ResetBase - takes 2-4 mins)...
Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase >> "%LOGFILE%" 2>&1
echo   Done.

:: ---------------------------------------------------------------------
:: 17. PURGING SYSTEM CRASH DUMPS, WER & TEMP
:: ---------------------------------------------------------------------
echo [17/18] Purging Crash Dumps, Windows Error Reports and Temp...
del /q /s /f "C:\Windows\Minidump\*" >> "%LOGFILE%" 2>&1
del /q /s /f "C:\Windows\Memory.dmp" >> "%LOGFILE%" 2>&1
del /q /s /f "C:\ProgramData\Microsoft\Windows\WER\ReportArchive\*" >> "%LOGFILE%" 2>&1
del /q /s /f "C:\ProgramData\Microsoft\Windows\WER\ReportQueue\*" >> "%LOGFILE%" 2>&1
del /q /s /f "C:\Windows\Temp\*" >> "%LOGFILE%" 2>&1
echo   Done.

:: ---------------------------------------------------------------------
:: 18. RESTARTING ESSENTIAL SERVICES
:: ---------------------------------------------------------------------
echo [18/18] Restarting background services...
net start "ClickToRunSvc" >nul 2>&1
net start "wslservice" >nul 2>&1
net start "ImControllerService" >nul 2>&1
net start "Lenovo Vantage Service" >nul 2>&1
net start "bits" >nul 2>&1
net start "wuauserv" >nul 2>&1

if exist "C:\Program Files\LGHUB\system_tray\lghub_system_tray.exe" (
    start "" "C:\Program Files\LGHUB\system_tray\lghub_system_tray.exe" --minimized >nul 2>&1
)

echo [FINISH] Admin Reclaim completed at %date% %time% >> "%LOGFILE%"
echo.
echo =====================================================================
echo    ALL ELEVATED CLEANUPS AND JUNCTIONS COMPLETE!
echo =====================================================================
echo Check your free space below:
powershell -Command "Get-PSDrive C, E | Select-Object Name, @{N='FreeGB';E={[math]::round($_.Free/1GB,2)}}, @{N='UsedGB';E={[math]::round($_.Used/1GB,2)}}"
echo.
echo Press any key to close this window.
pause >nul
