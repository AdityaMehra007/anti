@echo off
TITLE ADI CAREER OS — 'GET ME HIRED' Master Command Center
COLOR 0B

echo ===============================================================================
echo            ADI CAREER OS -- 'GET ME HIRED' MASTER CONTROL CENTER
echo ===============================================================================
echo Candidate : Aditya Mehra | BBA International Business (DSU '26) | Bengaluru
echo Objective : Maximize probability of securing top full-time job in Bangalore
echo Guardrail : 100%% Evidence-Verified | 100%% Sales Exclusion (Zero Cold Calling)
echo ===============================================================================
echo.
echo [1] Launch 'GET ME HIRED' Giant Interactive Web Dashboard (All 57 Subsystems)
echo [2] Run 'WHAT SHOULD I DO NEXT?' Single Highest-ROI Action Calculation
echo [3] View Today's Morning Job Briefing & Priorities
echo [4] Query AI Career Copilot in Terminal
echo [5] Launch Top 10 High-Affinity Bangalore Portals & Tailored ATS Resumes
echo [6] Open 61-Requisition Bangalore Application Hub
echo [7] Launch Bangalore Placement Agencies Studio & Portals (Top 15 Consultancies)
echo [8] Launch Bangalore 4,500 Companies Non-Stop Outreach Engine (Blitz Mode & Batches)
echo [9] Launch Bangalore Tech Parks & Campus Navigator (20 Premier Tech Parks)
echo [10] Launch Master AI Workforce & Capabilities Explorer (7,142 Agents & Skills)
echo [11] Run Full System Test Suite & Validation (Pytest + Integrity Checks)
echo [12] Exit
echo.
set /p choice="Select an option (1-12): "

if "%choice%"=="1" (
    echo.
    echo [*] Opening 'GET ME HIRED' Master Dashboard in browser...
    python adi_career_os_ultimate.py --dashboard
    goto end
)
if "%choice%"=="2" (
    echo.
    python adi_career_os_ultimate.py --next-action
    pause
    goto end
)
if "%choice%"=="3" (
    echo.
    python adi_career_os_ultimate.py --brief
    pause
    goto end
)
if "%choice%"=="4" (
    echo.
    set /p query="Enter your question for the AI Career Copilot: "
    python adi_career_os_ultimate.py --copilot "%query%"
    pause
    goto end
)
if "%choice%"=="5" (
    echo.
    python scripts/launch_bba_ib_strike.py --top10
    pause
    goto end
)
if "%choice%"=="6" (
    echo.
    python scripts/apply_all_bangalore.py --open-hub
    goto end
)
if "%choice%"=="7" (
    echo.
    echo [*] Launching Bangalore Job Agencies Studio...
    python scripts/apply_all_agencies_bangalore.py --open-agency-studio
    goto end
)
if "%choice%"=="8" (
    echo.
    echo [*] Launching Bangalore 4,500 Companies Non-Stop Outreach Engine...
    call LAUNCH_NON_STOP_OUTREACH.bat
    goto end
)
if "%choice%"=="9" (
    echo.
    echo [*] Launching Bangalore Tech Parks Directory Studio...
    python scripts/tech_park_dispatcher.py --open-studio
    goto end
)
if "%choice%"=="10" (
    echo.
    echo [*] Launching Master AI Workforce & Capabilities Explorer...
    python scripts/agent_skills_inspector.py --open-studio
    goto end
)
if "%choice%"=="11" (
    echo.
    python scripts/validate_all.py
    echo.
    pytest tests/test_ultimate_career_os.py tests/test_adi_career_os.py
    pause
    goto end
)

:end
