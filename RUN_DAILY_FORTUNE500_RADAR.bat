@echo off
TITLE Fortune 500 Bangalore Daily Job & Referral Radar
cd /d "e:\anti"
echo ======================================================================
echo    STARTING DAILY FORTUNE 500 BANGALORE JOB & REFERRAL RADAR
echo ======================================================================
echo Timestamp: %DATE% %TIME%
python daily_fortune500_bangalore_radar.py
echo.
echo ======================================================================
echo    CYCLE COMPLETE!
echo    View Dashboard: fortune_500_bangalore_radar.html
echo    View Markdown : FORTUNE_500_BANGLORE_DAILY_REFERRAL_RADAR.md
echo ======================================================================
pause
