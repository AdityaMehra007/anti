@echo off
setlocal enabledelayedexpansion

title CS Video Courses Intelligence Cockpit
color 0b

echo ========================================================================
echo   OMEGA / CS VIDEO COURSES INTELLIGENCE MISSION CONTROL COCKPIT
echo   Port: 8779 ^| Sourced from Developer-Y/cs-video-courses
echo ========================================================================
echo.

cd /d "%~dp0"

echo [1/3] Verifying and ensuring SQLite FTS5 database and roadmaps...
python -c "
from cs_courses_engine import CSCoursesEngine
from cs_courses_roadmaps import CSRoadmapsEngine
from pathlib import Path
if not Path('data/cs_video_courses.db').exists():
    print('Building database...')
    CSCoursesEngine().build_database()
if not Path('data/cs_role_roadmaps.json').exists():
    print('Building career roadmaps...')
    CSRoadmapsEngine().build_all_roadmaps()
print('Database and roadmaps verified.')
"

echo.
echo [2/3] Launching CS Video Courses API Server on http://localhost:8779...
start "" http://localhost:8779

echo.
echo [3/3] Running local server process (Press Ctrl+C to stop)...
python cs_courses_api_server.py 8779

pause
