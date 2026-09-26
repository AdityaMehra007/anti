<#
.SYNOPSIS
  OmniRoute Sovereign Gateway Management Script
.DESCRIPTION
  Provides 1-click status checks, dashboard launch, and prompt execution via OmniRoute.
#>

param(
    [Parameter(Position=0)]
    [ValidateSet("status", "dashboard", "test", "auto-chat", "help")]
    [string]$Action = "status",

    [Parameter(Position=1)]
    [string]$Prompt = "Hello from Antigravity!"
)

$OmniRouteUrl = "http://localhost:20128"

switch ($Action) {
    "status" {
        Write-Host "`n=== Checking OmniRoute Gateway Status ===" -ForegroundColor Cyan
        try {
            $resp = Invoke-WebRequest -Uri "$OmniRouteUrl/v1/models" -Method GET -TimeoutSec 3 -ErrorAction Stop
            Write-Host "[OK] OmniRoute Gateway is ACTIVE on $OmniRouteUrl" -ForegroundColor Green
        } catch {
            if ($_.Exception.Response.StatusCode -eq 401) {
                Write-Host "[OK] OmniRoute Gateway is ACTIVE on $OmniRouteUrl (Listening, Auth Gated)" -ForegroundColor Green
            } elseif ($_.Exception.Response.StatusCode -eq 404) {
                Write-Host "[OK] OmniRoute Gateway is ACTIVE on $OmniRouteUrl (Listening)" -ForegroundColor Green
            } else {
                Write-Host "[WARN] Gateway response: $($_.Exception.Message)" -ForegroundColor Yellow
            }
        }
        omniroute doctor
    }

    "dashboard" {
        Write-Host "`nOpening OmniRoute Dashboard in default browser: $OmniRouteUrl" -ForegroundColor Cyan
        Start-Process $OmniRouteUrl
    }

    "test" {
        Write-Host "`n=== Testing Zero-Config Auto Model (curl) ===" -ForegroundColor Cyan
        $body = @{
            model = "auto"
            messages = @(
                @{ role = "user"; content = $Prompt }
            )
        } | ConvertTo-Json -Compress

        try {
            $resp = Invoke-RestMethod -Uri "$OmniRouteUrl/v1/chat/completions" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 15
            Write-Host "`nResponse from Model: $($resp.model)" -ForegroundColor Green
            Write-Host "Content: $($resp.choices[0].message.content)`n" -ForegroundColor White
            if ($resp.choices[0].message.reasoning_content) {
                Write-Host "Reasoning: $($resp.choices[0].message.reasoning_content)`n" -ForegroundColor DarkGray
            }
            Write-Host "Tokens: Total=$($resp.usage.total_tokens) (Prompt=$($resp.usage.prompt_tokens), Completion=$($resp.usage.completion_tokens))" -ForegroundColor Cyan
        } catch {
            Write-Host "[ERROR] Request failed: $_" -ForegroundColor Red
        }
    }

    "auto-chat" {
        Write-Host "`n=== Sending CLI Chat via OmniRoute ===" -ForegroundColor Cyan
        omniroute chat $Prompt
    }

    "help" {
        Write-Host @"
OmniRoute Management Script:
  .\run_omniroute.ps1 status       - Check server health and doctor diagnostics
  .\run_omniroute.ps1 dashboard    - Open web dashboard at http://localhost:20128
  .\run_omniroute.ps1 test [prompt]- Send test request to zero-config 'auto' model
  .\run_omniroute.ps1 auto-chat    - Interactive chat prompt through OmniRoute CLI
"@
    }
}
