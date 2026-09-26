@echo off
TITLE ADI CAREER OS — BBA International Business Bangalore Strike Engine
COLOR 0A

echo ===============================================================================
echo       ADI CAREER OS -- BBA INTERNATIONAL BUSINESS BANGALORE STRIKE ENGINE
echo ===============================================================================
echo Candidate : Aditya Mehra
echo Degree    : BBA International Business (DSU '26) | CGPA 6.33/10
echo Location  : Bengaluru, Karnataka (Immediate Availability)
echo Flagships : Aero India 2025 Lead Ops | Puma & Tata Comm Ops | Instawork AI QA
echo Guardrail : 100%% Sales Exclusion (Zero Cold Calling / Zero Telecalling)
echo ===============================================================================
echo.
echo [1] Launch Top 10 High-Affinity Bangalore Portals + Tailored ATS Resumes
echo [2] Launch 61-Requisition Master Strike Studio (Full Interactive Hub)
echo [3] Launch 4,500 Bangalore Employers Mega-Studio (Mailto Directory)
echo [4] Launch Target 300 Global Strike Board
echo [5] Launch Bangalore Job Placement Agencies Studio & Portals (Top 15 Consultancies)
echo [6] View Top 10 High-Affinity BBA IB Roles & Details
echo [7] Run Zero-Hallucination Evidence & System Audit
echo [8] Exit
echo.
set /p choice="Select an option (1-8): "

if "%choice%"=="1" (
    echo.
    echo [*] Launching Top 10 Target Career Portals and Tailored Resumes...
    python scripts/launch_bba_ib_strike.py --top10
    pause
    goto end
)
if "%choice%"=="2" (
    echo.
    echo [*] Opening 61-Requisition Master Strike Studio...
    python scripts/launch_bba_ib_strike.py --all-hub
    goto end
)
if "%choice%"=="3" (
    echo.
    echo [*] Opening 4,500 Bangalore Employers Mega-Studio...
    python scripts/apply_all_bangalore.py --open-mega
    goto end
)
if "%choice%"=="4" (
    echo.
    echo [*] Opening Target 300 Strike Board...
    python scripts/apply_all_bangalore.py --open-300
    goto end
)
if "%choice%"=="5" (
    echo.
    echo [*] Opening Bangalore Job Agencies Studio & Portals...
    python scripts/apply_all_agencies_bangalore.py --open-agency-studio
    goto end
)
if "%choice%"=="6" (
    echo.
    python scripts/launch_bba_ib_strike.py --list
    pause
    goto end
)
if "%choice%"=="7" (
    echo.
    python scripts/apply_all_bangalore.py --audit
    pause
    goto end
)

:end
