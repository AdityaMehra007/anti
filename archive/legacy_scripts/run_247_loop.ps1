$logFile = "e:\anti\247_career_loop.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$entry = "[$timestamp] [24/7 CAREER ENGINE] Active 24/7 Autonomous Cycle Executed successfully.`n"
Add-Content -Path $logFile -Value $entry
Write-Host $entry
