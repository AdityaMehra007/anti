@echo off
setlocal
cd /d "%~dp0"

echo =======================================================
echo   JOBSPY BANGALORE CAREER SCRAPER & STRIKE BOARD SYNC
echo =======================================================
echo Candidate: Aditya Mehra (DSU Bangalore '26)
echo Target Corridors: ORR Bellandur, Koramangala, Whitefield, Hebbal
echo Target Roles: B2B Sales / BD, AI Data Ops, EXIM, Founders Office
echo.

python jobspy_market_scraper.py --sites indeed google linkedin naukri --limit 10 --hours 72 --min-score 80 --sync-board

echo.
echo =======================================================
echo   INGESTION COMPLETE
echo =======================================================
pause
