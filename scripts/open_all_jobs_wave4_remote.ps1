# WAVE 4: Open all 35 Remote-First Company Career Pages
# Usage: powershell -ExecutionPolicy Bypass -File open_all_jobs_wave4_remote.ps1

$links = @(
    "https://stripe.com/jobs",
    "https://zapier.com/jobs",
    "https://scale.com/careers",
    "https://supabase.com/careers",
    "https://vercel.com/careers",
    "https://www.deel.com/careers",
    "https://remote.com/careers",
    "https://canonical.com/careers",
    "https://automattic.com/work-with-us/",
    "https://buffer.com/journey",
    "https://doist.com/careers",
    "https://ghost.org/careers/",
    "https://careers.hotjar.com/",
    "https://www.hubspot.com/careers",
    "https://close.com/careers/",
    "https://customer.io/careers/",
    "https://duckduckgo.com/hiring",
    "https://www.elastic.co/careers/",
    "https://kinsta.com/careers/",
    "https://www.okta.com/company/careers/",
    "https://www.omnipresent.com/careers",
    "https://www.stickermule.com/careers",
    "https://www.toptal.com/careers",
    "https://www.helpscout.com/careers/",
    "https://kit.com/careers",
    "https://www.formstack.com/careers",
    "https://lemon.io/careers/",
    "https://mercor.com",
    "https://outlier.ai",
    "https://www.a.team/careers",
    "https://x-team.com/careers/",
    "https://www.timedoctor.com/careers",
    "https://clevertech.biz/careers",
    "https://platform.sh/company/careers/",
    "https://www.zyte.com/careers/"
)

Write-Host "=== WAVE 4: Opening 35 Remote-First Company Career Pages ===" -ForegroundColor Cyan
Write-Host "Cover letters are in: e:\anti\applications_generated\REMOTE_*\" -ForegroundColor Yellow
Write-Host ""

$batch = 0
foreach ($link in $links) {
    $batch++
    Start-Process $link
    Start-Sleep -Milliseconds 800
    if ($batch % 10 -eq 0 -and $batch -lt $links.Count) {
        Write-Host "  Opened $batch / $($links.Count) — pausing 5s..." -ForegroundColor Green
        Start-Sleep -Seconds 5
    }
}

Write-Host ""
Write-Host "=== All 35 remote career pages opened! Browse & apply. ===" -ForegroundColor Green
