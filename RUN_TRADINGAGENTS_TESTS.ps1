# PowerShell Launcher for TradingAgents Automated Test Suite
$ErrorActionPreference = "Stop"
$ProjectDir = Join-Path $PSScriptRoot "projects\TradingAgents"
Set-Location $ProjectDir

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host " TradingAgents: Verification & Test Suite Runner" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan

$PytestExe = Join-Path $ProjectDir ".venv\Scripts\pytest.exe"
if (-not (Test-Path $PytestExe)) {
    Write-Error "Pytest executable not found at $PytestExe"
}

& $PytestExe tests/test_omni_integration.py -v
