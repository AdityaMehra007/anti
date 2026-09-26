@echo off
chcp 65001 >nul
title ADITYA GLOBAL CAREER INTELLIGENCE OS — COMMAND CENTER
cd /d "e:\anti"

:MENU
cls
echo ===============================================================================
echo        ADITYA GLOBAL CAREER INTELLIGENCE OS (VERSION 1.0)
echo        Owner: Aditya Mehra ^| BBA International Business (DSU '26)
echo        Target Track: Non-Sales Corporate Operations, Analytics, PMO, EXIM
echo ===============================================================================
echo.
echo   [W] LAUNCH INTERACTIVE WEB COCKPIT (ADITYA_CAREER_INTELLIGENCE_COCKPIT.html)
echo   [H] MASTER HR DIRECTORY: 7,500 NAMES, NUMBERS ^& EMAILS (/hr-directory)
echo   [1] VIEW TODAY'S TOP 10 ACTION QUEUE (/top-10)
echo   [2] VIEW ALL ACTIVE & VERIFIED JOBS (/jobs-today)
echo   [3] SCAN BENGALURU CORRIDORS & COMPANIES (/scan-bangalore)
echo   [4] DISCOVER VERIFIED RECRUITERS (/scan-recruiters)
echo   [5] DISCOVER HIRING MANAGERS & OPS LEADERS (/scan-hiring-managers)
echo   [6] FIND EMPLOYEE & ALUMNI REFERRAL PATHWAYS (/find-referrals)
echo   [7] VIEW APPLICATIONS PIPELINE (/applications)
echo   [8] VIEW INTERVIEW CRM & PREP PACKS (/interviews)
echo   [9] RUN COMPLETE REFRESH & GENERATE MASTER EXCEL (/refresh-data)
echo   [E] OPEN MASTER EXCEL WORKBOOK (ADI_GLOBAL_CAREER_INTELLIGENCE.xlsx)
echo   [C] EXPORT CLEAN CSV DATASETS (/export-csv)
echo   [A] RUN DATA QUALITY & AUDIT REPORT (/audit-data)
echo   [T] RUN AUTOMATED PYTEST SUITE
echo   [0] EXIT
echo.
echo ===============================================================================
set /p CHOICE="Select an option: "

if /i "%CHOICE%"=="W" start "" "ADITYA_CAREER_INTELLIGENCE_COCKPIT.html" & goto MENU
if /i "%CHOICE%"=="H" python aditya_global_career_intelligence_os.py /hr-directory & pause & goto MENU
if /i "%CHOICE%"=="1" python aditya_global_career_intelligence_os.py /top-10 & pause & goto MENU
if /i "%CHOICE%"=="2" python aditya_global_career_intelligence_os.py /jobs-today & pause & goto MENU
if /i "%CHOICE%"=="3" python aditya_global_career_intelligence_os.py /scan-bangalore & pause & goto MENU
if /i "%CHOICE%"=="4" python aditya_global_career_intelligence_os.py /scan-recruiters & pause & goto MENU
if /i "%CHOICE%"=="5" python aditya_global_career_intelligence_os.py /scan-hiring-managers & pause & goto MENU
if /i "%CHOICE%"=="6" python aditya_global_career_intelligence_os.py /find-referrals & pause & goto MENU
if /i "%CHOICE%"=="7" python aditya_global_career_intelligence_os.py /applications & pause & goto MENU
if /i "%CHOICE%"=="8" python aditya_global_career_intelligence_os.py /interviews & pause & goto MENU
if /i "%CHOICE%"=="9" python aditya_global_career_intelligence_os.py /refresh-data & pause & goto MENU
if /i "%CHOICE%"=="E" start "" "ADI_GLOBAL_CAREER_INTELLIGENCE.xlsx" & goto MENU
if /i "%CHOICE%"=="C" python aditya_global_career_intelligence_os.py /export-csv & pause & goto MENU
if /i "%CHOICE%"=="A" python aditya_global_career_intelligence_os.py /audit-data & pause & goto MENU
if /i "%CHOICE%"=="T" pytest tests/test_career_intelligence_system.py & pause & goto MENU
if /i "%CHOICE%"=="0" exit /b
goto MENU
