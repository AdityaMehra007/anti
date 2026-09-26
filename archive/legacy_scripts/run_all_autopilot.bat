@echo off
TITLE Aditya Mehra AI Autopilot Career Launcher
COLOR 0A

echo ================================================================================
echo                🚀 ADITYA MEHRA AI AUTOPILOT CAREER LAUNCHER
echo ================================================================================
echo Candidate: Aditya Mehra | BBA International Business (Dayananda Sagar Univ)
echo Target: Bangalore MNCs & Fortune 500 Companies
echo ================================================================================
echo.

echo [1/5] Copying Tailored Cover Letter to Windows Clipboard...
powershell -Command "Set-Clipboard -Value (Get-Content -Path 'e:\anti\Cover_Letters_All_MNCs.txt' -Raw)"
echo ✅ Cover Letter Copied to Clipboard! (Press Ctrl+V on webforms to paste)

echo.
echo [2/5] Opening Interactive AI Dashboard...
start "" "e:\anti\index.html"
echo ✅ Dashboard Opened!

echo.
echo [3/5] Launching Top MNC & Fortune 500 Application Portals...
powershell -Command "Start-Process 'https://careers.walmart.com/'; Start-Process 'https://www.amazon.jobs/en/locations/bangalore-india'; Start-Process 'https://careers.google.com/locations/bangalore/'; Start-Process 'https://careers.microsoft.com/'; Start-Process 'https://www.accenture.com/in-en/careers'; Start-Process 'https://www2.deloitte.com/ui/en/careers/careers.html'; Start-Process 'https://www.ey.com/en_in/careers'; Start-Process 'https://www.goldmansachs.com/careers/'"
echo ✅ All Application Portals Opened in Browser!

echo.
echo [4/5] Opening 1-Click Recruiter Email Drafts...
start "" "e:\anti\Email_Drafts\Email_Draft_Accenture.eml"
start "" "e:\anti\Email_Drafts\Email_Draft_Deloitte.eml"
start "" "e:\anti\Email_Drafts\Email_Draft_EY.eml"
start "" "e:\anti\Email_Drafts\Email_Draft_Amazon.eml"
start "" "e:\anti\Email_Drafts\Email_Draft_GoldmanSachs.eml"
echo ✅ Recruiter Email Drafts Opened!

echo.
echo [5/5] Opening Application Tracking Sheet...
start "" "e:\anti\Application_Tracker.csv"
echo ✅ Application Tracker Opened in Excel/Spreadsheets!

echo.
echo ================================================================================
echo                🎉 AUTOPILOT LAUNCH COMPLETE! ALL PORTALS ARE READY!
echo ================================================================================
pause
