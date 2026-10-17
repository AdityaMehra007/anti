@echo off
TITLE Mega Top 500 Startups & Fortune 500 MNC Daily Radar
cd /d "e:\anti"
echo ======================================================================
echo    STARTING MEGA TOP 500 STARTUPS & FORTUNE 500 MNC JOB & REFERRAL RADAR
echo ======================================================================
echo Timestamp: %DATE% %TIME%
python mega_startups_and_f500_radar.py
echo.
echo ======================================================================
echo    RADAR CYCLE COMPLETE!
echo    View Dashboard: mega_startups_and_f500_radar.html
echo    View Markdown : MEGA_TOP500_STARTUPS_AND_F500_MNC_RADAR.md
echo ======================================================================
pause
