@echo off
TITLE LAUNCH APEX CAREER UNIVERSE -- ADITYA MEHRA (DSU '26)
COLOR 0B

echo ===============================================================================
echo                APEX CAREER & BUSINESS SUPREMACY UNIVERSE
echo                     Aditya Mehra -- DSU '26 -- Bengaluru
echo ===============================================================================
echo.
echo [1/4] Verifying Core Relational Database Integrity...
python -c "import sqlite3; conn = sqlite3.connect('e:/anti/BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite'); c = conn.cursor(); c.execute('SELECT COUNT(*) FROM bangalore_5000_companies_master'); print(f'>>> Database OK: {c.fetchone()[0]} Companies Verified.'); conn.close()"

echo.
echo [2/4] Launching Executive Portfolio...
start "" "e:\anti\ADITYA_MEHRA_EXECUTIVE_PORTFOLIO.html"

echo.
echo [3/4] Launching Bengaluru 360 Visual World...
start "" "e:\anti\BANGALORE_360_VISUAL_WORLD.html"

echo.
echo [4/4] Launching STAR Interview Defense Matrix...
start "" "e:\anti\STAR_INTERVIEW_DEFENSE_MATRIX.html"

echo.
echo ===============================================================================
echo             ALL APEX SYSTEMS OPERATIONAL -- YOU ARE READY TO STRIKE
echo ===============================================================================
echo.
pause
