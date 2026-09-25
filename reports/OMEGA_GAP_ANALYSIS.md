# ?? OMEGA ECOSYSTEM GAP ANALYSIS & UNFINISHED WORK

| Desired Capability | Current State | Blocker / Dependency | Effort | Priority | Next Action |
|---|---|---|---|---|---|
| **Live SMTP / OAuth Dispatch** | `PREPARED` | Requires user-provided OAuth2 / App Password credentials | Low | High | Configure `.env` with authenticated SMTP/LinkedIn connector. |
| **Real-Time Job Feeds (Adzuna/Indeed)** | `SEEDED_AUDITED` | Requires live webhook/API aggregator integration | Medium | Medium | Integrate Firecrawl / job RSS scraper into `opportunity_engine.py`. |
| **Voice-Enabled Interview Simulator** | `LOCAL_EVAL` | Web Speech API integration in browser UI | Low | Low | Add speech synthesis & dictation to `interview_simulator.html`. |
| **Automated Follow-up Sentinel** | `LOCAL_SCAN` | Integrates with persistent cron runner | Low | Medium | Schedule `run_omni_daemon.py` via Windows Task Scheduler. |
