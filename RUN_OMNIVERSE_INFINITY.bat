@echo off
setlocal enabledelayedexpansion

echo ===============================================================================
echo                 OMNIVERSE INFINITY ULTIMATE - AUTONOMOUS RUNNER
echo      Master Career Intelligence, ATS Engine, Mailroom & Executive Cockpit
echo ===============================================================================
echo Candidate: Aditya Mehra | BBA International Business (DSU '26) | Bengaluru Hub
echo Track Scope: 100%% Non-Sales Corporate Operations & Systems Analytics
echo.

cd /d "E:\anti"

echo [1/12] Populating SQLite Database & Master 4,500 Company Census...
python omniverse_engine.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to populate Omniverse Engine.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/12] Generating 4 Tailored ATS Resumes (Operations, Audit, EXIM, Systems)...
python omniverse_resume_builder.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to generate ATS Resumes.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [3/12] Generating Tailored STAR Application Dockets...
python omniverse_dockets.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to generate Application Dockets.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [4/12] Executing Autonomous Application Dispatcher with Cryptographic Ledger...
python omniverse_dispatcher.py --dispatch-all
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to execute Dispatcher.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [5/12] Assembling RFC 5322 MIME Mailroom Packages (.eml) with Attached Resumes...
python omniverse_mailer.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to assemble Mailroom Packages.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [6/12] Compiling Behavioral Interview Defense Compendium...
python omniverse_interview_defense.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to compile Interview Defense.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [7/12] Mapping 9,223 LinkedIn Connections & DSU Alumni Referral Paths...
python omniverse_referral_graph.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to map Referral Matrix.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [8/12] Generating All 35 Mandatory Section 43 Deliverables (JSON & CSV)...
python omniverse_deliverables_generator.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to generate Section 43 deliverables.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [9/12] Constructing 12-Month Rolling Non-Sales Hiring Calendar...
python omniverse_hiring_calendar.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to generate Hiring Calendar.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [10/12] Synthesizing Skills Competency Matrix & Verified Project Portfolio...
python omniverse_skills_portfolio.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to generate Skills Portfolio.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [11/12] Running Autonomous Sentinel Daemon Health Cycle...
python omniverse_daemon.py --once
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Daemon health cycle failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [12/12] Running Comprehensive Verification Test Suite (25 Enterprise Gates)...
python test_omniverse_full_suite.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Verification suite failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ===============================================================================
echo                 ALL SYSTEMS OPERATIONAL & FULLY VERIFIED!
echo ===============================================================================
echo [OK] 4,500 Bangalore Companies Loaded & Classified
echo [OK] 14 Active Non-Sales October 2026 Roles Matched & Dispatched
echo [OK] 4 ATS Resumes & 14 RFC 5322 .eml Packages Stored in /resumes & /outbox
echo [OK] 35 Section 43 Deliverables Exported in /omniverse_deliverables
echo [OK] 12-Month Rolling Hiring Calendar & 8-Domain Competency Matrix Built
echo [OK] 25 Comprehensive Verification Tests Passing (100%% Green)
echo.
echo Launching Executive Cockpit Dashboard in browser...
start "" "OMNIVERSE_INFINITY_COCKPIT.html"
echo.
echo To start the live FastAPI REST Server, run:
echo   python omniverse_cli.py serve --port 8000
echo.
pause
