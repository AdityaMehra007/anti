@echo off
echo [!] Starting Fortune 500 Autonomous Factory...
python fortune_500_factory.py
echo.
echo [!] Running Pytest Verification Suite...
python -m pytest fortune_500_projects/test_fortune500_all_sectors.py -v
pause
