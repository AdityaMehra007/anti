# WAVE 2: Open all 39 Indeed Job Listings for Apply
# Usage: powershell -ExecutionPolicy Bypass -File open_all_jobs_wave2_indeed.ps1

$links = @(
    "http://in.indeed.com/job/ai-operations-associate-voice-quality-data-81e684220bd06600",
    "http://in.indeed.com/job/business-development-associate-011d313090c2988e",
    "http://in.indeed.com/job/business-development-associate-295dc6998d6edc0c",
    "http://in.indeed.com/job/business-development-associate-325cd44bcda910c0",
    "http://in.indeed.com/job/business-development-associate-3e3cf1f95cd44f01",
    "http://in.indeed.com/job/business-development-associate-4a83c81b9c4a2100",
    "http://in.indeed.com/job/business-development-associate-4ad91a8cb85b0686",
    "http://in.indeed.com/job/business-development-associate-4e62f09d9fcc1333",
    "http://in.indeed.com/job/business-development-associate-553421f1ed65a4ce",
    "http://in.indeed.com/job/business-development-associate-5ec7cd893664f970",
    "http://in.indeed.com/job/business-development-associate-6708d50f47ec37f6",
    "http://in.indeed.com/job/business-development-associate-6794c1ca25b65f1c",
    "http://in.indeed.com/job/business-development-associate-6be8ba53636b61cc",
    "http://in.indeed.com/job/business-development-associate-8128f7804060df77",
    "http://in.indeed.com/job/business-development-associate-aadfe2a08603b0c8",
    "http://in.indeed.com/job/business-development-associate-abb30b9b7e725657",
    "http://in.indeed.com/job/business-development-associate-bda-57bb1aae89d7e06f",
    "http://in.indeed.com/job/business-development-associate-d1cd400ce5e35b3a",
    "http://in.indeed.com/job/business-development-associate-ddf3cb2df1f382db",
    "http://in.indeed.com/job/business-development-associate-fresher-85bdb5f370883a23",
    "http://in.indeed.com/job/business-development-associate-fresher-experienced-bengaluru-f4358e691c147ab7",
    "http://in.indeed.com/job/business-development-associate-inside-sales-326b3fb6065a11f8",
    "http://in.indeed.com/job/business-development-associate-presales-b2b-corporate-relations-893c61c7e31f189b",
    "http://in.indeed.com/job/business-development-executive-bde-08fb5d1bf084b59c",
    "http://in.indeed.com/job/business-development-executive-bde-6a0a25112f01edef",
    "http://in.indeed.com/job/business-development-executive-bde-faa16bcc6ccba80e",
    "http://in.indeed.com/job/business-development-executive-international-sales-73096ee63824a36f",
    "http://in.indeed.com/job/business-development-intern-e22f75be9e6cdb91",
    "http://in.indeed.com/job/content-associate-05fd20a6e7625179",
    "http://in.indeed.com/job/finance-associate-40d8bd4970f7bf49",
    "http://in.indeed.com/job/founders-associate-business-development-growth-db75bc24dc14b3d3",
    "http://in.indeed.com/job/offline-trainer-sr-executive-assistant-manager-7e7d3597c121622d",
    "http://in.indeed.com/job/outbound-marketing-specialist-b2b-lead-generation-8ce04221eaa8e71b",
    "http://in.indeed.com/job/pre-sales-associate-pre-sales-executive-51b715e1e9d305fa",
    "http://in.indeed.com/job/research-analyst-df865b83f35a0624",
    "http://in.indeed.com/job/sales-manager-5660ed3fc10bd68f",
    "http://in.indeed.com/job/sales-managerbusiness-manager-761e1413a7cec2b8",
    "http://in.indeed.com/job/sales-process-associate-14137999da0ca59e",
    "http://in.indeed.com/job/sales-revenue-operations-specialist-e6bb7d81da6d340f"
)

Write-Host "=== WAVE 2: Opening 39 Indeed Job Links ===" -ForegroundColor Cyan
Write-Host "Have your Indeed resume uploaded first!" -ForegroundColor Yellow
Write-Host ""

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
Write-Host "=== All 39 Indeed jobs opened! Apply to each tab. ===" -ForegroundColor Green
