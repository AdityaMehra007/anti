# WAVE 1: Open all 40 LinkedIn Job Postings for Quick Apply
# Usage: Right-click > Run with PowerShell, or: powershell -ExecutionPolicy Bypass -File open_all_jobs_wave1_linkedin.ps1

$links = @(
    "https://www.linkedin.com/jobs/view/4472489769",
    "https://www.linkedin.com/jobs/view/4472402998",
    "https://www.linkedin.com/jobs/view/4471392194",
    "https://www.linkedin.com/jobs/view/4468448421",
    "https://www.linkedin.com/jobs/view/4468087592",
    "https://www.linkedin.com/jobs/view/4467999249",
    "https://www.linkedin.com/jobs/view/4467885990",
    "https://www.linkedin.com/jobs/view/4467855474",
    "https://www.linkedin.com/jobs/view/4467849888",
    "https://www.linkedin.com/jobs/view/4467730055",
    "https://www.linkedin.com/jobs/view/4467724190",
    "https://www.linkedin.com/jobs/view/4467557291",
    "https://www.linkedin.com/jobs/view/4466508501",
    "https://www.linkedin.com/jobs/view/4466262219",
    "https://www.linkedin.com/jobs/view/4466195708",
    "https://www.linkedin.com/jobs/view/4465613591",
    "https://www.linkedin.com/jobs/view/4465580437",
    "https://www.linkedin.com/jobs/view/4465406105",
    "https://www.linkedin.com/jobs/view/4465054678",
    "https://www.linkedin.com/jobs/view/4465040248",
    "https://www.linkedin.com/jobs/view/4464869641",
    "https://www.linkedin.com/jobs/view/4464863195",
    "https://www.linkedin.com/jobs/view/4464842855",
    "https://www.linkedin.com/jobs/view/4464838762",
    "https://www.linkedin.com/jobs/view/4464763563",
    "https://www.linkedin.com/jobs/view/4464683780",
    "https://www.linkedin.com/jobs/view/4464526120",
    "https://www.linkedin.com/jobs/view/4464268717",
    "https://www.linkedin.com/jobs/view/4464172965",
    "https://www.linkedin.com/jobs/view/4463980099",
    "https://www.linkedin.com/jobs/view/4463956686",
    "https://www.linkedin.com/jobs/view/4463950440",
    "https://www.linkedin.com/jobs/view/4463809641",
    "https://www.linkedin.com/jobs/view/4463416826",
    "https://www.linkedin.com/jobs/view/4463243629",
    "https://www.linkedin.com/jobs/view/4463240225",
    "https://www.linkedin.com/jobs/view/4463093898",
    "https://www.linkedin.com/jobs/view/4462381098",
    "https://www.linkedin.com/jobs/view/4455913778",
    "https://www.linkedin.com/jobs/view/4435689604"
)

Write-Host "=== WAVE 1: Opening 40 LinkedIn Job Links ===" -ForegroundColor Cyan
Write-Host "Make sure you're logged into LinkedIn first!" -ForegroundColor Yellow
Write-Host ""

# Open in batches of 10 to avoid browser crash
$batch = 0
foreach ($link in $links) {
    $batch++
    Start-Process $link
    Start-Sleep -Milliseconds 800
    if ($batch % 10 -eq 0 -and $batch -lt $links.Count) {
        Write-Host "  Opened $batch / $($links.Count) — pausing 5s before next batch..." -ForegroundColor Green
        Start-Sleep -Seconds 5
    }
}

Write-Host ""
Write-Host "=== All 40 LinkedIn jobs opened! Quick Apply each tab. ===" -ForegroundColor Green
