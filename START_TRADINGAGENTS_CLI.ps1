# PowerShell Launcher for TradingAgents CLI
$ErrorActionPreference = "Stop"
$ProjectDir = Join-Path $PSScriptRoot "projects\TradingAgents"
Set-Location $ProjectDir

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host " TradingAgents: Multi-Agent LLM Financial Trading Framework (CLI)" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan

$PythonExe = Join-Path $ProjectDir ".venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Error "Python virtual environment not found at $PythonExe"
}

& $PythonExe -m cli.main
