---
name: interview-simulator-pro
description: Real-world mock interview coach and STAR/CAR response generator tailored to company interview loops and candidate's verified proof points.
---

# INTERVIEW SIMULATOR PRO

Simulates company-specific interview loops, draws real questions from the knowledge vault, and delivers structured STAR behavioral answers.

## Capabilities
- Pulls company-specific interview loops (HR Screen, Cognitive/Case, Functional Manager, Bar-Raiser).
- Maps every behavioral question to Aditya's verified proof points:
  - High-Stakes Operations: Aero India 2025 (100k+ attendees, 0 breaches, 0% shrinkage).
  - Cost Optimization: 15% recurring savings via direct tier-1 vendor rate cards across Bangalore.
  - Commercial B2B Sales: Closed INR 1.5L+ commercial revenue at Pencil Mark.
  - Quality Precision: 99%+ accuracy at Instawork AI data ops.
- Curveball Defense: Ready answers for "Why BBA over engineering?", "What if a supplier fails 2 hours before a launch?", and "Where do you see yourself in 3-5 years?".

## Python Usage
```python
from apex_career_os.agents.interview_master import InterviewMasterAgent

interview = InterviewMasterAgent()
prep = interview.generate_interview_prep_pack("Accenture", "Operations Analyst")

print("Company Culture:", prep["company_culture_dna"])
for qa in prep["tailored_qa_bank"]:
    print("Q:", qa["question"])
    print("STAR Result:", qa["recommended_star_framework"]["result"])
```
