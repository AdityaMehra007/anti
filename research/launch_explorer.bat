@echo off
echo Starting System Prompts Intelligence Explorer on port 8080...
start "" "http://localhost:8080/system_prompts_explorer.html"
python -m http.server 8080 --directory "%~dp0"
