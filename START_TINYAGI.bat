@echo off
title TinyAGI Core Daemon & API Server (Port 3777)
cd /d "e:\anti\tinyagi"
echo =======================================================
echo   TinyAGI Daemon - Multi-Agent / Queue Engine (Port 3777)
echo =======================================================
echo Starting TinyAGI main process...
node packages/main/dist/index.js
pause
