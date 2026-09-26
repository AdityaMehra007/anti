@echo off
title Stop Project NOMAD
cd /d "e:\anti\project-nomad"
echo Stopping Project NOMAD containers...
docker compose -f docker-compose.windows.yml down
echo Project NOMAD stopped.
pause
