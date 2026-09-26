@echo off
:: Check for Admin Privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] This script must be run as Administrator!
    echo Please right-click this file and select "Run as administrator".
    pause
    exit /b 1
)

echo =====================================================================
echo    ANTIGRAVITY OMEGA - ELEVATED C: DRIVE SPACE RECLAIMER
echo =====================================================================
echo.

:: 1. Purge Obsolete update backup folders
echo [1/5] Removing obsolete LGHUB update backups (203 MB)...
if exist "C:\Program Files\LGHUB.old" (
    rmdir /s /q "C:\Program Files\LGHUB.old"
    echo Removed C:\Program Files\LGHUB.old.
)

:: 2. Purge Windows Update Download Cache (~900 MB)
echo [2/5] Purging Windows Update Download Cache (900 MB)...
net stop wuauserv >nul 2>&1
net stop bits >nul 2>&1
del /q /s /f "C:\Windows\SoftwareDistribution\Download\*" >nul 2>&1
for /d %%p in ("C:\Windows\SoftwareDistribution\Download\*") do rmdir /s /q "%%p" >nul 2>&1
net start bits >nul 2>&1
net start wuauserv >nul 2>&1
echo Done.

:: 3. Dism Component Store Cleanup (reclaims 3 to 5 GB from WinSxS)
echo [3/5] Cleaning superseded Windows components (WinSxS /ResetBase)...
Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase
echo Done.

:: 4. Clean Windows Error Reporting and Crash Dumps
echo [4/5] Purging Crash Dumps and System Logs...
del /q /s /f "C:\Windows\Minidump\*" >nul 2>&1
del /q /s /f "C:\Windows\Memory.dmp" >nul 2>&1
del /q /s /f "C:\ProgramData\Microsoft\Windows\WER\ReportArchive\*" >nul 2>&1
del /q /s /f "C:\ProgramData\Microsoft\Windows\WER\ReportQueue\*" >nul 2>&1
echo Done.

:: 5. Clean Temp
echo [5/5] Purging Windows Temp...
del /q /s /f "C:\Windows\Temp\*" >nul 2>&1
echo Done.

echo.
echo =====================================================================
echo    ALL ELEVATED CLEANUPS COMPLETE!
echo =====================================================================
pause
