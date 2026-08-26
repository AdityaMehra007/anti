# OMEGA UNFINISHED WORK AUDIT

1. **Firecrawl Active Web Scraping**:
   - MCP server is registered in catalog.
   - Next step: Call Firecrawl tool from `live_job_discovery.py` to extract Workday and Taleo pages.
2. **Persistent Background Scheduler**:
   - Create PowerShell script `register_omega_daemon.ps1` to schedule daily morning runs at 08:00 IST.
3. **Application Dispatch Integration**:
   - Integrate Playwright / browser automation for human-approved portal application pre-filling.
