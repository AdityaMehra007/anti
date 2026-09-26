@echo off
title Project NOMAD - WSL2 Linux Setup
cls
echo ==========================================================
echo        PROJECT NOMAD - WSL2 NATIVE LINUX SETUP            
echo ==========================================================
echo.
echo Checking WSL status...
wsl.exe --status
echo.
echo Installing / Opening Ubuntu on WSL2...
echo (If prompted, please complete initial Unix user creation)
echo.
wsl.exe --install -d Ubuntu

echo.
echo ==========================================================
echo Next step: inside your Ubuntu terminal, run:
echo.
echo sudo apt-get update ^&^& sudo apt-get install -y curl ^&^& curl -fsSL https://raw.githubusercontent.com/Crosstalk-Solutions/project-nomad/refs/heads/main/install/install_nomad.sh -o install_nomad.sh ^&^& sudo bash install_nomad.sh
echo.
echo ==========================================================
pause
