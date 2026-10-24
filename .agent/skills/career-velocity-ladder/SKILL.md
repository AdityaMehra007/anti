---
name: career-velocity-ladder
description: Beyond-job career strategy, 30-60-90 day onboarding dominance, multi-year promotion ladders, compensation negotiation, and executive positioning.
---

# CAREER VELOCITY LADDER

Architects the candidate's trajectory beyond landing the job: onboarding excellence, fast-track promotions, salary negotiation leverage, and executive positioning.

## Capabilities
- Day 30-60-90 Onboarding Blueprint:
  - Day 1-30: Operational Absorption & Seam Discovery.
  - Day 31-60: Vendor Standardization & Automated Dashboarding.
  - Day 61-90: High-Leverage Strategic Ownership & ROI Impact Dossier.
- 5-Year Hyper-Growth Roadmap:
  - Year 1: High-Performance Associate (₹7.0L - ₹11.0L CTC)
  - Year 2-3: Operations Lead / Senior BD Manager (₹14.0L - ₹22.0L CTC)
  - Year 4-5: Founders' Office / Chief of Staff / Operations Director (₹35.0L - ₹50.0L+ CTC + ESOPs)
- Market Compensation Benchmark & Offer Negotiation Playbook:
  - P25, Median P50, P75, and P90 benchmarks for Bangalore.
  - Phone and email counter-offer scripts anchoring on verified metrics.

## Python Usage
```python
from apex_career_os.agents.compensation_strategist import CompensationStrategistAgent
from apex_career_os.agents.career_growth_architect import CareerGrowthArchitectAgent

comp = CompensationStrategistAgent()
benchmark = comp.benchmark_role_compensation("Operations & Vendor Governance")
playbook = comp.generate_negotiation_playbook("Deloitte", offered_ctc_lpa=6.0, target_ctc_lpa=8.0)

growth = CareerGrowthArchitectAgent()
blueprint = growth.generate_30_60_90_day_blueprint("Deloitte", "Operations Analyst")
ladder = growth.generate_5_year_career_ladder()
```
