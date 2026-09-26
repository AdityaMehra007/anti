@echo off
title SOVEREIGN CAREER COPILOT
color 0E

python "%~dp0ai_career_copilot.py" status
echo.
echo Commands available:
echo   python ai_career_copilot.py list
echo   python ai_career_copilot.py pitch BLR-JOB-001
echo   python ai_career_copilot.py cover BLR-JOB-001
echo   python ai_career_copilot.py interview Accenture
echo   python ai_career_copilot.py ask "Your question"
echo.
cmd /k
