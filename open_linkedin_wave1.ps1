# PowerShell script to open Top 10 Verified LinkedIn Recruiters in default browser
# Run: powershell -ExecutionPolicy Bypass -File .\open_linkedin_wave1.ps1

Write-Host "Opening Top 10 Verified LinkedIn Recruiters for Aditya Mehra..." -ForegroundColor Cyan

$recruiters = @(
    "https://www.linkedin.com/search/results/people/?keywords=Volvo%20Group%20Bangalore%20HR%20Recruiter",
    "https://jobs.boeing.com/job/bengaluru/associate-procurement-agent/185/141289825",
    "https://www.linkedin.com/in/samiksha-sharma1470", # Accenture
    "https://www.linkedin.com/in/aditi-tayde",        # Deloitte
    "https://www.linkedin.com/in/deepashree-r-4bb8b11a1", # EY
    "https://www.linkedin.com/in/sangini-sahay-4779b424b", # Amazon
    "https://www.linkedin.com/in/syed-sumbul-shahbaz-b53210107", # Goldman Sachs
    "https://www.linkedin.com/in/shweta-sheregar-985b341a",      # JP Morgan
    "https://www.linkedin.com/in/sandhya-b-sriram-06b02047",     # IBM
    "https://www.linkedin.com/in/kohely-ghosal"                  # KPMG
)

foreach ($url in $recruiters) {
    Write-Host "Opening: $url" -ForegroundColor Green
    Start-Process $url
    Start-Sleep -Milliseconds 800
}

Write-Host "All tabs opened! Open LINKEDIN_RECRUITER_DISPATCHER.html to copy personalized 300-char notes." -ForegroundColor Yellow
