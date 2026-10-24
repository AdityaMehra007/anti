---
name: recruiter-network-strike
description: Direct access to Aditya Mehra's 9,223 LinkedIn connections and verified Bangalore HR Directory to identify hiring managers and generate high-conversion outreach sequences.
---

# RECRUITER NETWORK STRIKE AGENT

Leverages Aditya Mehra's 9,223 LinkedIn connections, 1,449 direct HR contacts, and 736 C-Suite executives to bypass ATS gatekeepers.

## Capabilities
- Rapid fuzzy search across Bangalore Tech Corridors (Bellandur, Whitefield, Manyata, Electronic City, Koramangala).
- Direct access to recruiter names, designations, corporate email addresses, and LinkedIn search URLs.
- Generates 3-Stage Outreach Packs:
  1. Stage 1: Cold Email / InMail linking verified achievements (Aero India, 15% procurement savings, 0 days notice).
  2. Stage 2: Value-Add Follow-up (Day 4: Vendor management & B2B pipeline case study).
  3. Alumni / Warm Referral Request (customized for mutual contacts).

## Python Usage
```python
from apex_career_os.agents.network_strike import NetworkStrikeAgent

network = NetworkStrikeAgent()
recruiters = network.find_recruiters_for_company("Deloitte", limit=5)

for r in recruiters:
    print(f"Recruiter: {r['name']} ({r['title']}) - {r['email']}")

# Generate personalized outreach pack
outreach = network.generate_outreach_dossier(
    {"company": "Deloitte", "title": "Business Advisory Analyst"},
    contact=recruiters[0]
)
print(outreach["stage_1_cold_email"])
```
