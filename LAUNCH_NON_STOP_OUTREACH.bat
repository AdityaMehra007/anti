@echo off
chcp 65001 >nul
title ADI CAREER OS - BANGALORE 4,500 COMPANIES NON-STOP OUTREACH ENGINE
color 0B

:MENU
cls
echo ========================================================================================
echo        ADI CAREER OS — BANGALORE 4,500 COMPANIES NON-STOP OUTREACH ENGINE
echo       Candidate: Aditya Mehra ^| BBA International Business '26 ^| Phone: +91 70034 56624
echo ========================================================================================
echo.
echo   [1] Launch Non-Stop Outreach Studio (Web GUI with 1-Click Send ^& Blitz Mode)
echo   [2] Generate 50 Ready-to-Send EML Drafts (Next Batch)
echo   [3] Generate 100 Ready-to-Send EML Drafts (Next Batch)
echo   [4] Open EML Outbox Folder (applications_generated/mega_4500_eml_outbox)
echo   [5] View Live Outreach Statistics ^& Progress across 4,500 Targets
echo   [6] Open Master 4,500 CSV in Excel (BANGALORE_4500_ALL_COMPANIES_NON_STOP_OUTREACH.csv)
echo   [7] Exit
echo.
echo ========================================================================================
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto STUDIO
if "%choice%"=="2" goto BATCH50
if "%choice%"=="3" goto BATCH100
if "%choice%"=="4" goto OUTBOX
if "%choice%"=="5" goto STATUS
if "%choice%"=="6" goto CSV
if "%choice%"=="7" goto EXIT

echo Invalid choice! Please select 1-7.
timeout /t 2 >nul
goto MENU

:STUDIO
echo.
echo Launching Non-Stop Outreach Studio in your default browser...
start http://localhost:9119/apps/job_application_studio/bangalore_non_stop_outreach_studio.html
goto PAUSE_MENU

:BATCH50
echo.
echo Generating next 50 RFC-822 EML drafts...
python scripts/non_stop_outreach_dispatcher.py --generate-batch 50
echo.
echo Drafts generated! Opening outbox folder...
python scripts/non_stop_outreach_dispatcher.py --open-outbox
goto PAUSE_MENU

:BATCH100
echo.
echo Generating next 100 RFC-822 EML drafts...
python scripts/non_stop_outreach_dispatcher.py --generate-batch 100
echo.
echo Drafts generated! Opening outbox folder...
python scripts/non_stop_outreach_dispatcher.py --open-outbox
goto PAUSE_MENU

:OUTBOX
echo.
echo Opening EML outbox folder...
python scripts/non_stop_outreach_dispatcher.py --open-outbox
goto PAUSE_MENU

:STATUS
echo.
python scripts/non_stop_outreach_dispatcher.py --status
goto PAUSE_MENU

:CSV
echo.
echo Opening Master 4,500 Companies CSV in Excel...
start "" "BANGALORE_4500_ALL_COMPANIES_NON_STOP_OUTREACH.csv"
goto PAUSE_MENU

:PAUSE_MENU
echo.
echo Press any key to return to menu...
pause >nul
goto MENU

:EXIT
echo.
echo Exiting Non-Stop Outreach Engine. Good luck with your applications!
timeout /t 1 >nul
exit /b 0
