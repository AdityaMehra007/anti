# PowerShell Launcher for TradingAgents Streamlit Web Cockpit
$ErrorActionPreference = "Stop"
$ProjectDir = Join-Path $PSScriptRoot "projects\TradingAgents"
Set-Location $ProjectDir

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host " TradingAgents: Autonomous Web Cockpit (Streamlit)" -ForegroundColor Green
Write-Host " Opening GUI at http://localhost:8501" -ForegroundColor Yellow
Write-Host "=====================================================================" -ForegroundColor Cyan

$StreamlitExe = Join-Path $ProjectDir ".venv\Scripts\streamlit.exe"
if (-not (Test-Path $StreamlitExe)) {
    Write-Error "Streamlit executable not found at $StreamlitExe"
}

& $StreamlitExe run app.py
