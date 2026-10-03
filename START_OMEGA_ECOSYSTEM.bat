@echo off
TITLE ANTIGRAVITY OMEGA — Enterprise Subsystem Launcher
COLOR 0B

echo =========================================================================
echo       ANTIGRAVITY OMEGA :: ENTERPRISE SYSTEM LAUNCHER (LEVEL-X)
echo =========================================================================
echo [1/3] Activating Python virtual environment...
if exist "e:\anti\.venv\Scripts\activate.bat" (
    call e:\anti\.venv\Scripts\activate.bat
)

echo [2/3] Launching Fault-Tolerant Daemon Supervisor on port 8095...
start "Omega Supervisor Daemon" cmd /k "python e:\anti\aios\services\omega_supervisor.py 8095"

echo [3/3] Opening Master Executive HUD (Single-Pane Console)...
start http://localhost:3000

echo =========================================================================
echo All subsystems registered with auto-restart supervisor.
echo - Master HUD:            http://localhost:3000
echo - Supervisor API:        http://localhost:8095/status
echo - AI Gateway:            http://localhost:8090/v1/health
echo - TradeNexus B2B:        http://localhost:8000
echo - Plane CE Workspaces:   http://localhost:80
echo =========================================================================
pause
