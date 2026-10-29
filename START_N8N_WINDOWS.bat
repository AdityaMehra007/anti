@echo off
TITLE n8n Enterprise Workflow Platform & Agent Engine
SETLOCAL EnableDelayedExpansion

echo ========================================================
echo   n8n ENTERPRISE WORKFLOW PLATFORM & AGENT ENGINE
echo   OMEGA Autonomous Platform & Node DAG Core
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/3] Verifying n8n SDK and database assets...
python -c "import n8n_orchestrator; client = n8n_orchestrator.N8nClient(); print(f'[OK] Node Catalog: {len(client.mock.nodes)} nodes | Workflows: {len(client.mock.workflows)}')"

echo.
echo [2/3] Executing 12-Phase Sovereign Verification...
python n8n_cli.py do-everything

echo.
echo [3/3] Opening n8n Mission Control Cockpit...
start "" "n8n_control_cockpit.html"

echo.
echo ========================================================
echo   Starting local n8n API Server on port 8771...
echo ========================================================
python n8n_api_server.py --port 8771
