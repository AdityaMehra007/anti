# CAREER HQ — TOOL MAP

| Tool Name | Engine / Script | Purpose | Execution Mode |
| :--- | :--- | :--- | :---: |
| `omega status` | `omega/control_tower/cli.py` | System health, model telemetry, and verification state | CLI Command |
| `omega live-scan` | `omega/career_war_room/live_job_discovery.py` | Live API job discovery and reachability verification | CLI Command |
| `omega top-jobs` | `omega/career_war_room/live_job_discovery.py` | Display top confirmed live openings | CLI Command |
| `omega target-companies` | `omega/career_war_room/company_intelligence.py` | Inspect 20 verified Bengaluru GCC hubs | CLI Command |
| `omega funnel-status` | `omega/career_war_room/career_analytics.py` | Ground truth application and pipeline funnel | CLI Command |
| `omega war-room` | `omega/career_war_room/career_brain.py` | Master daily career intelligence briefing | CLI Command |
| `omega backup` | `omega/engines/disaster_recovery.py` | Disaster recovery snapshot generation | CLI Command |
