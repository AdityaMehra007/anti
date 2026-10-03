# WAVE 3: Open all 37 ATS/Workday/Direct Portal Job Links
# Usage: powershell -ExecutionPolicy Bypass -File open_all_jobs_wave3_ats.ps1

$links = @(
    "https://abb.wd3.myworkdayjobs.com/External_Career_Page/job/Bangalore-Karnataka-India/Associate-Project-Engineer_JR00045022",
    "https://abb.wd3.myworkdayjobs.com/External_Career_Page/job/Bangalore-Karnataka-India/Associate-Project-Manager_JR00041299",
    "https://alliancedata.wd5.myworkdayjobs.com/en-US/breadfinancial_India/job/Bangalore-India/Bangalore-Process-Associate_R1013166",
    "https://bakertilly.wd5.myworkdayjobs.com/BTCareers/job/IND-KA-Bangalore---Cherry-Hills/Associate-Test-Automation-Engineer_JR107350",
    "https://careersen-herbalife.icims.com/jobs/20150/job",
    "https://careersen-herbalife.icims.com/jobs/20442/job",
    "https://cloudifyops.zohorecruit.in/jobs/Careers/78115000017247736/Associate-Technical-Project-Manager",
    "https://cnx.wd1.myworkdayjobs.com/external_global/job/IND-Bangalore---Karle-Town-Centre-13th-Flr-Nagawara-Village/sr-Team-leader_R1763739",
    "https://datamaticstechnologies.applytojob.com/apply/oHnkB0EPEi/AI-Platform-Operations-Engineer",
    "https://db.wd3.myworkdayjobs.com/en-US/DBWebsite/job/Bangalore-Raheja-Towers-26-27-M-G-Road/Trade-and-Transaction-Operator--NCT_R0405862-1",
    "https://db.wd3.myworkdayjobs.com/en-US/DBWebsite/job/Bangalore-Velankani-Tech-Park/Associate---Payroll-Control_R0450952",
    "https://db.wd3.myworkdayjobs.com/en-US/DBWebsite/job/Bangalore-Velankani-Tech-Park/KYC-Associate_R0447603",
    "https://diageo.wd3.myworkdayjobs.com/en-US/Diageo_Careers/job/Bangalore-India/Process-Analyst--HR-Operations_JR1128498",
    "https://enterpriseplatform.dell.com:443/hcmUI/CandidateExperience/en/job/298440",
    "https://epicorsoftware.wd5.myworkdayjobs.com/en-US/epicorjobs/job/India-Bangalore/Tech-App-Specialist--ERP-Support-_JR104910",
    "https://firstadvantage.wd5.myworkdayjobs.com/FirstAdvantage/job/IN_Bangalore_Office/EA-US-PR---Team-Leader_R10213",
    "https://firstam.wd1.myworkdayjobs.com/faicareers/job/IND-Karnataka-Bangalore/Quality-Assurance-Analyst_R058557",
    "https://genpact.wd108.myworkdayjobs.com/External_Careers/job/1401-G-India-1-6-FL-Surya-Park-STPI-Bangalore/Sr-Analyst---Process-Analytics---S-M-4A_JR10026258",
    "https://genpact.wd108.myworkdayjobs.com/External_Careers/job/1401-G-India--Pritech-Park-4-F-SEZ-II-Bangalore/Sr-Associate---F-A---I2C-5B_JR10014538",
    "https://genpact.wd108.myworkdayjobs.com/External_Careers/job/1401-GIPL-Prestige-Technology-Park-IV-Bangalore/Analyst---Business-Data-Services-5A_JR10020474",
    "https://genpact.wd108.myworkdayjobs.com/External_Careers/job/1401-GIPL-Prestige-Technology-Park-IV-Bangalore/Associate---S-P---Procurement-Ops-5A_JR10026685",
    "https://genpact.wd108.myworkdayjobs.com/External_Careers/job/1401-GIPL-Prestige-Technology-Park-IV-Bangalore/Specialist---SCM---Logistics-Support-4A_JR10022158",
    "https://genpact.wd108.myworkdayjobs.com/External_Careers/job/1401-GIPL-Prestige-Technology-Park-IV-Bangalore/Sr-Developer---Application-Development-JAVA-N-4B_JR10025151",
    "https://genpact.wd108.myworkdayjobs.com/External_Careers/job/1401-GIPL-Prestige-Technology-Park-IV-Bangalore/Sr-Developer---Application-Development-JAVA-S-4B_JR10025354",
    "https://genpact.wd108.myworkdayjobs.com/External_Careers/job/1401-GIPL-Prestige-Technology-Park-IV-Bangalore/Tech-Lead---Application-Development-JAVA-N-4C_JR10027845",
    "https://gtssc.ripplehire.com/candidate/?token=uATZP1OfBiW6W5vV1BYU&source=CAREERSITE#detail/job/907150",
    "https://indiacareers-paychex.icims.com/jobs/45368/job",
    "https://ingrammicro.wd5.myworkdayjobs.com/en-US/IngramMicro/job/Bengaluru-India/Key-Account-Manager_R-115179",
    "https://jda.wd5.myworkdayjobs.com/en-US/JDA_Careers/job/Bangalore/Sr-Technical-Consultant---Middleware-Support-SQL-Python-Snowflake_262816",
    "https://jobs.lever.co/weekdayworks/020f460e-1b92-474e-86c0-62a7be21740b",
    "https://kapturecrm.keka.com/careers/jobdetails/161708",
    "https://levistraussandco.wd5.myworkdayjobs.com/External/job/GCC-Office--ITC-Green-Center-Bengaluru-Karnataka-India/Associate-Engineer--SAP-Basis_R-0152933",
    "https://pixxel.darwinbox.in/ms/candidate/careers/a6aa3f5789682d",
    "https://revantage.wd1.myworkdayjobs.com/Revantage/job/Bengaluru/Associate-Legal-Counsel_JR104173",
    "https://revantage.wd1.myworkdayjobs.com/Revantage/job/Bengaluru/Sr-Associate---DevOps_JR104219-1",
    "https://zebra.wd501.myworkdayjobs.com/en-US/Zebra_careers/job/Bengaluru-India/Manager--Data-Scientist_JR103256",
    "https://1lattice.recruiterbox.com/jobs/fk0ztlp?fjb_hash=ezLpq610"
)

Write-Host "=== WAVE 3: Opening 37 ATS/Workday Portal Links ===" -ForegroundColor Cyan
Write-Host "These require full registration + resume upload on each portal." -ForegroundColor Yellow
Write-Host "Resume to use: Aditya_Mehra_Master_ATS_Resume_Bangalore.pdf" -ForegroundColor Yellow
Write-Host ""

$batch = 0
foreach ($link in $links) {
    $batch++
    Start-Process $link
    Start-Sleep -Milliseconds 1000
    if ($batch % 8 -eq 0 -and $batch -lt $links.Count) {
        Write-Host "  Opened $batch / $($links.Count) — pausing 8s (ATS portals are heavier)..." -ForegroundColor Green
        Start-Sleep -Seconds 8
    }
}

Write-Host ""
Write-Host "=== All 37 ATS portals opened! Register + upload resume on each. ===" -ForegroundColor Green
