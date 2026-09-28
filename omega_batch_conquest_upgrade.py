#!/usr/bin/env python3
"""
========================================================================================
OMEGA BATCH CONQUEST ENGINE — UNIVERSAL UPGRADE & MASS DEPLOYMENT
========================================================================================
Scans ALL 254 existing application folders, reads their APPLICATION_MANIFEST.json,
and generates the MISSING assets for each company:
  - ATS_RESUME.md
  - STAR_INTERVIEW_DEFENSE.md
  - DAY_30_60_90_PLAN.md
  - COMPENSATION_NEGOTIATION.md
  - MASTER_CONQUEST_INDEX.md (unified index)

Preserves existing assets. Only generates what's missing.
========================================================================================
"""

import os
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"e:\anti\applications_generated")

# ── Verified Candidate Truth Ledger ─────────────────────────────────────────
CANDIDATE = {
    "name": "Aditya Mehra",
    "location": "Bengaluru, Karnataka, India",
    "phone": "+91 7003456624",
    "email": "ashishiash007@gmail.com",
    "alt_email": "adityamehra799@gmail.com",
    "linkedin": "linkedin.com/in/adityamehra",
    "education": "Bachelor of Business Administration (BBA) in International Business",
    "institution": "Dayananda Sagar University (DSU), Bengaluru",
    "grad_year": "2026",
}

# ── Asset Generators ────────────────────────────────────────────────────────

def gen_ats_resume(company: str, role: str, ctc: str = "") -> str:
    ctc_line = f"  **Target CTC:** {ctc}" if ctc else ""
    return f"""# {CANDIDATE['name'].upper()}
**{CANDIDATE['location']}** | **Phone:** {CANDIDATE['phone']} | **Email:** {CANDIDATE['email']} | **LinkedIn:** {CANDIDATE['linkedin']}

---

## PROFESSIONAL SUMMARY
Results-driven **{CANDIDATE['education']}** graduate specializing in high-velocity operations, vendor optimization, and client pipeline execution. Proven capability delivering **300+ high-stakes operational deployments** for marquee tier-1 enterprise accounts including **Tata Communications, Puma India, and Aero India 2025**. Championed direct procurement restructuring delivering a **15% recurring operational cost reduction** and independently generated **INR 1.5L+ in commercial B2B revenue**. Seeking to drive scalable operational excellence and cross-functional performance as **{role}** at **{company}**.{ctc_line}

---

## CORE COMPETENCIES & KEYWORD ALIGNMENT
- **Operations & Execution:** End-to-End Operational Logistics, Cross-Functional Team Leadership (20+ crew), Vendor Rate Card Negotiation, Budgetary Governance, SLA Adherence, Process Optimization.
- **Commercial & Strategic Analysis:** B2B Client Pipeline Management, Cost-Benefit Analysis, Resource Allocation, Risk Mitigation, 15% Procurement Optimization, Stakeholder Reporting.
- **Global Trade & Supply Chain:** EXIM Procedures, Incoterms 2020, Customs Clearance (ICD Whitefield), UCP 600 Letters of Credit (LC), Landed Cost Calculations, DGFT Compliance.
- **Technical & Analytical Stack:** Advanced MS Excel (XLOOKUP, Pivot Tables, Data Modelling), Power BI, Tableau, CRM Automation (HubSpot/Salesforce), Python Scripting, SQL Fundamentals, AI Workflow Evaluation.

---

## PROFESSIONAL EXPERIENCE

### Event Operations Lead & Project Coordinator — Self-Employed / Freelance
*Bengaluru, India | Jan 2021 – Present*
- Orchestrated on-ground operations and cross-functional vendor management for **300+ enterprise and marquee events**, managing budgets end-to-end with **0% budget overrun** and 100% on-time milestone delivery.
- Directed on-site operations for premier accounts including **Aero India 2025 (Yelahanka Air Force Station)**, **Tata Communications**, **Puma India**, and **VH1 Supersonic** music festival.
- Led cross-functional teams of **20+ on-ground staff** spanning venue setup, security protocols, technical infrastructure, and VIP guest relations under strict SLA deadlines.
- Conducted root-cause vendor analysis and restructured rate agreements, eliminating intermediate agency markups to achieve a **15% direct cost reduction** across recurring operational expenditure.

### Operations Lead (Aero India 2025) — Salt in My Coca
*Bengaluru, India | Feb 2025*
- Orchestrated end-to-end commercial stall operations, high-value inventory control, and VIP delegation engagement at **Asia's largest aerospace expo** with 15,000+ daily attendees.
- Ensured 100% adherence to rigorous IAF defense facility compliance, security passes, and time-critical delivery constraints across multi-day expo sessions with zero non-conformances.

### Business Development Executive Intern — Pencil Mark Interior Solutions LLP
*Bengaluru, India | Jul 2025 – Aug 2025*
- Spearheaded outbound B2B corporate client acquisition, qualifying high-value commercial architectural and interior projects across Bangalore's tech corridor.
- Independently prospected, pitched, and converted client accounts generating **INR 1.5L+ in direct commercial revenue** within first 6 weeks.
- Awarded formal **written management commendation** for surpassing outreach quotas and accelerating lead-to-close conversion speed by 25%.

### AI Data Operations & Quality Specialist — Instawork AI
*Remote / Bengaluru | Sep 2024 – Dec 2024*
- Executed high-precision multi-modal data curation, prompt annotation, and quality assurance benchmarks for production LLM models.
- Maintained an audited **99%+ accuracy rating** across thousands of evaluation batches, enforcing strict validation taxonomy and edge-case categorization.

### Chief Executive Officer / Operations Manager — Family Business
*Kolkata, India | Jan 2018 – Nov 2020*
- Led day-to-day operations across sales, marketing, cash flow management, and client administration for a multi-category retail enterprise.
- Restructured procurement and vendor coordination workflows, achieving a **15% reduction in recurring overhead costs** and improved supplier payment cycles.

---

## EDUCATION

### Bachelor of Business Administration (BBA) — International Business Specialization
**Dayananda Sagar University (DSU)**, Bengaluru, Karnataka | *Graduation: 2026*
- Core Focus: Strategic Operations, International Trade & EXIM, Corporate Finance, Business Analytics, Negotiation & Contract Law, Organizational Behavior.

---

## AWARDS, COMMENDATIONS & CERTIFICATIONS
- **Written Management Commendation:** Pencil Mark Interior Solutions LLP (Exemplary B2B Business Development & Client Conversion Performance).
- **Tier-1 Enterprise Operational Delivery:** Verified lead coordinator for Tata Communications, Puma India, and Aero India 2025 (IAF Yelahanka).
- **AI Data Quality Certification:** 99%+ Benchmark Accuracy at Instawork AI Multi-Modal Evaluation.
"""


def gen_interview_pack(company: str, role: str) -> str:
    return f"""# 360° STAR/CAR INTERVIEW PREPARATION & DEFENSE MATRIX
**Company:** {company} | **Role:** {role}
**Candidate:** {CANDIDATE['name']} | **Generated:** {datetime.now().strftime('%Y-%m-%d')}

---

## PART 1: TOP 5 BEHAVIORAL QUESTIONS (STAR METHOD)

### Q1: "Tell me about a time you handled a high-pressure operational crisis."
- **Situation:** At Aero India 2025 (Asia's largest defense and aerospace expo at Yelahanka Air Force Station), I managed commercial booth logistics and VIP visitor operations under IAF security clearance.
- **Task:** On Day 1 morning, critical inventory shipment was delayed at the security checkpoint due to protocol changes, threatening an empty stall during VIP delegation rounds.
- **Action:** I immediately mobilized with the IAF liaison officer, presented pre-verified documentation and gate passes, and coordinated with the on-ground transport crew to fast-track security inspection. In parallel, I rearranged display priorities with existing floor materials to ensure the pavilion was presentation-ready 15 minutes before VIP entry.
- **Result:** 100% booth uptime achieved. Over 500+ defense dignitaries and VIPs were successfully engaged. Zero stock loss or protocol infractions recorded.

### Q2: "How have you driven measurable cost reduction without hurting quality?"
- **Situation:** Across freelance operations coordinating large-scale corporate events and brand activations (Puma, Tata Communications), recurring vendor invoices were eroding project margins by 12-18% due to middleman markups.
- **Task:** Protect profit margins while guaranteeing flawless on-time milestone delivery.
- **Action:** Performed a granular line-item audit of staging, AV equipment, fabrication, and transport expenses. Mapped direct source suppliers in Bangalore and bypassed third-party aggregator agencies. Negotiated tiered volume rate cards with primary vendors in exchange for multi-event commitments.
- **Result:** Delivered a recurring **15% operational cost reduction** across subsequent projects, saving significant capital while maintaining 100% client satisfaction ratings.

### Q3: "Give an example of closing a commercial deal with a skeptical client."
- **Situation:** At Pencil Mark Interior Solutions, commercial real estate developers were hesitant to commit to new interior fit-out partners during economic tightening.
- **Task:** Generate qualified meetings and close commercial contracts independently.
- **Action:** Researched client lease timelines and created tailored cost-per-square-foot ROI comparisons instead of generic brochures. Conducted disciplined direct outreach, followed up within 2 hours of inquiry, and walked decision-makers through transparent material specifications.
- **Result:** Closed **INR 1.5L+ in commercial contract revenue** within 6 weeks. Received formal written management commendation for breaking previous outreach records.

### Q4: "How do you maintain precision when working on repetitive data tasks?"
- **Situation:** At Instawork AI, I was part of a specialized team annotating multi-modal dataset batches and verifying LLM benchmark responses.
- **Task:** Internal SLA of 95% audit accuracy under tight turnaround deadlines.
- **Action:** Created a personal validation rubric and pre-submission checklist, cross-referencing edge-case labeling rules before batch submission. Documented ambiguous prompts and collaborated with QA leads to normalize categorization standards.
- **Result:** Maintained **99%+ audit accuracy** across thousands of prompt-response evaluations, ranking in the top quartile of the team.

### Q5: "How do you lead teams without formal hierarchical authority?"
- **Situation:** During large brand activations (VH1 Supersonic), I managed 20+ crew members across security, sound engineers, caterers, and stagehands from independent external vendors.
- **Task:** Ensure synchronicity across stage transitions under rigid broadcast timings.
- **Action:** Held 15-minute pre-event alignment briefings establishing clear individual accountability, set up instant two-way radio protocol, and led by example working side-by-side on high-friction bottlenecks.
- **Result:** Every stage transition executed within the allotted 3-minute window with zero logistical delay.

---

## PART 2: TOP 3 CURVEBALL DEFENSE SCRIPTS

### Curveball 1: "You are a 2026 graduate. Why hire you over someone with 3-5 years corporate experience?"
> "Experienced candidates often bring legacy habits, fixed processes, and higher compensation requirements. I bring 4+ years of verified, on-ground battlefield experience—having coordinated 300+ live deployments, managed 20-person teams, and driven 15% cost savings before even graduating. I have no bad corporate habits to unlearn, the stamina and hunger of someone building their career, and fresh analytical grounding from DSU. You get someone who executes on Day 1 with high ownership and zero entitlement."

### Curveball 2: "Your background spans events, commercial interiors, and AI data. How is this relevant to {role} at {company}?"
> "Every role I've held revolves around one core capability: delivering operational excellence under constraints. In events—300+ deployments with zero margin for error. In business development—revenue pipeline discipline and cost estimation. In AI data—absolute analytical precision. {role} at {company} requires exactly this combination: vendor governance, cross-functional coordination, and analytical rigor."

### Curveball 3: "What is your biggest professional weakness?"
> "Early on, I took on too much operational load myself instead of delegating, believing personal execution was the only way to ensure quality. During a multi-vendor corporate setup, I realized this created a single point of failure. I solved this by developing standardized SOP checklists and delegating specific zones to trained leads with a clear check-in cadence. That shift is what allowed me to scale from small events to managing 300+ large-scale deployments."

---

## PART 3: 5 KILLER REVERSE-INTERVIEW QUESTIONS FOR {company.upper()}

1. *"If I'm hired into {role}, what is the single biggest operational bottleneck you'd like to see completely resolved within my first 90 days?"*
2. *"How does this team balance long-term process optimization with day-to-day firefighting, and where has friction been highest recently?"*
3. *"What distinguishes operators who merely perform adequately from those who become indispensable leaders across {company}?"*
4. *"Looking at {company}'s strategic goals for the next 12 months, what new systems or workflows will this team need to build?"*
5. *"Based on our conversation today, is there any aspect of my background you'd like me to clarify further?"*
"""


def gen_plan90(company: str, role: str) -> str:
    return f"""# 30-60-90 DAY STRATEGIC ONBOARDING BLUEPRINT
**Company:** {company} | **Role:** {role}
**Candidate:** {CANDIDATE['name']} | **Generated:** {datetime.now().strftime('%Y-%m-%d')}

---

## PHASE 1: DAYS 1 – 30 | ABSORB, AUDIT & ALIGN

**Goal:** Achieve 100% workflow fluency, map cross-functional dependencies, and identify quick-win operational friction points.

| Week | Key Milestones |
|------|----------------|
| 1 | Complete all company onboarding modules, compliance protocols, IT access, and system setup. |
| 1-2 | Conduct 1-on-1 discovery interviews with direct team, cross-functional partners, and key vendors. |
| 2-3 | Perform comprehensive audit of existing SOPs, tracking spreadsheets, ticketing workflows, and vendor contracts. |
| 3-4 | Identify 2-3 "quick-win" process bottlenecks that can be streamlined without disrupting core operations. |
| 4 | Deliver a **30-Day Synthesis Memo** to direct manager summarizing operational observations and proposed efficiency targets. |

**Deliverable:** Written diagnostic report with 2-3 actionable improvement proposals.

---

## PHASE 2: DAYS 31 – 60 | EXECUTE, OPTIMIZE & DELIVER QUICK WINS

**Goal:** Assume autonomous ownership of daily operational streams and implement structured process improvements.

| Week | Key Milestones |
|------|----------------|
| 5-6 | Take full, unassisted ownership of core operational queues, vendor check-ins, and SLA tracking. |
| 6-7 | Implement standardized rate card tracking or workflow checklists (modeled after 15% cost optimization methodology). |
| 7-8 | Reduce reporting turnaround time by introducing automated Excel / Power BI dashboard views for weekly management reviews. |
| 8 | Proactively troubleshoot vendor or cross-team delivery escalations before SLA breach. Hold mid-quarter alignment review with manager. |

**Deliverable:** First measurable efficiency gain (10-15% turnaround or cost improvement) documented.

---

## PHASE 3: DAYS 61 – 90 | SCALE, OWN & DELIVER MEASURABLE ROI

**Goal:** Drive measurable bottom-line value, codify institutional best practices, and free up managerial bandwidth.

| Week | Key Milestones |
|------|----------------|
| 9-10 | Operate with complete autonomy as the go-to operational problem-solver for the division. |
| 10-11 | Publish updated, hardened SOP documentation so any new team member can onboard with zero disruption. |
| 11-12 | Deliver measurable business impact: 10-15% reduction in turnaround time or operational cost leakage across assigned streams. |
| 12 | Present a **90-Day Value Summary** to leadership highlighting verified metrics, closed projects, and recommended H2 operational initiatives. |

**Deliverable:** Executive presentation with quantified ROI, operational improvements, and forward-looking roadmap.
"""


def gen_negotiation(company: str, ctc: str = "") -> str:
    # Parse target CTC range if available
    t_min, t_max = "7.5", "11.0"
    if ctc:
        import re
        nums = re.findall(r'[\d.]+', ctc)
        if len(nums) >= 2:
            t_min, t_max = nums[0], nums[1]
        elif len(nums) == 1:
            t_min = nums[0]
            t_max = str(float(nums[0]) * 1.3)

    return f"""# HIGH-STAKES COMPENSATION NEGOTIATION PLAYBOOK
**Company:** {company} | **Target CTC Band:** ₹{t_min}L – ₹{t_max}L LPA
**Candidate:** {CANDIDATE['name']} | **Generated:** {datetime.now().strftime('%Y-%m-%d')}

---

## RULE 1: NEVER STATE A NUMBER FIRST IN EARLY SCREENS

## SCRIPT A: Deflecting Salary Expectations in Round 1
> **HR:** *"What are your current salary expectations?"*
> **{CANDIDATE['name']}:** *"Right now, my primary focus is finding the right operational fit where I can make an immediate, tangible impact at {company}. I'm confident {company} provides competitive compensation aligned with Bangalore market standards for high-performing operators. Once we confirm I'm the best fit for the team's needs, I'm sure we'll agree on a fair number. Could you share the allocated budget range for this position?"*

---

## SCRIPT B: Countering a Low Initial Offer
> **HR:** *"We're pleased to offer you the position with a package of ₹X CTC."*
> **{CANDIDATE['name']}:** *"Thank you so much. I'm genuinely thrilled about the opportunity to join {company}. Based on my research on the market benchmark for this role in Bangalore, and considering the verified track record I bring—having managed 300+ operational deployments, delivered a 15% cost optimization, and proven commercial closing capability—I was expecting an offer in the ₹{t_min}L to ₹{t_max}L range. If we can adjust the package closer to ₹{t_min}L, I would be ready to sign and commit immediately. Is there flexibility to make that adjustment?"*

---

## SCRIPT C: Negotiating Non-Salary Levers (If Base is Capped)
> **{CANDIDATE['name']}:** *"I completely understand if the base salary band is capped by internal company policy for this level. To bridge the gap, would {company} be open to considering:*
> 1. *A one-time joining/retention bonus of ₹75,000 – ₹1,00,000?*
> 2. *An accelerated performance appraisal review at 6 months instead of 12 months, tied to specific KPI milestones?*
> 3. *A hybrid flexibility allowance or educational certification sponsorship?*
> *Any of these options would make this a definitive decision for me."*

---

## SCRIPT D: Final Acceptance & Commitment
> **{CANDIDATE['name']}:** *"I appreciate you working with leadership to make this happen. I am 100% committed to delivering exceptional value for {company} and look forward to hitting the ground running on Day 1. Please send over the revised offer letter and I will sign it right away."*

---

## CRITICAL ANCHORING RULES
1. **Never accept the first number.** Always counter respectfully with value evidence.
2. **Anchor to verified metrics:** 300+ operations, 15% cost savings, INR 1.5L+ revenue, 99%+ accuracy.
3. **If base is truly fixed**, negotiate joining bonus, review cycle acceleration, and flexibility.
4. **Express genuine enthusiasm** throughout — enthusiasm + data = maximum leverage.
"""


def gen_master_index(company: str, role: str, folder_path: Path) -> str:
    files = sorted([f.name for f in folder_path.iterdir() if f.is_file()])
    file_list = "\n".join([f"- [{f}]({f})" for f in files])
    return f"""# 🏆 OMEGA APEX COMPLETE CONQUEST PACK: {company.upper()}
**Role:** {role}
**Candidate:** {CANDIDATE['name']}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Complete Application & Interview Assets
{file_list}

---
*Generated by OMEGA Universal Batch Conquest Engine v10.0*
"""


# ── Main Batch Processor ───────────────────────────────────────────────────

def process_all_folders():
    if not BASE_DIR.exists():
        print(f"[ERROR] Base directory not found: {BASE_DIR}")
        return

    folders = sorted([d for d in BASE_DIR.iterdir() if d.is_dir()])
    total = len(folders)
    upgraded = 0
    skipped = 0
    errors = 0

    print(f"\n{'='*72}")
    print(f"  OMEGA BATCH CONQUEST ENGINE — UNIVERSAL UPGRADE DEPLOYMENT")
    print(f"  Total Company Folders: {total}")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*72}\n")

    for i, folder in enumerate(folders, 1):
        company_name = folder.name
        role = "Operations & Business Development Specialist"
        ctc = ""

        # Try to read manifest for role/company/CTC details
        manifest_path = folder / "APPLICATION_MANIFEST.json"
        if manifest_path.exists():
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                company_name = manifest.get("company", folder.name)
                role = manifest.get("role", role)
                ctc = manifest.get("ctc", "")
            except (json.JSONDecodeError, KeyError):
                pass

        # Clean company name for display
        display = company_name[:55]

        # Generate missing assets
        generated = []
        try:
            # 1. ATS Resume
            resume_path = folder / "ATS_RESUME.md"
            if not resume_path.exists():
                resume_path.write_text(gen_ats_resume(company_name, role, ctc), encoding="utf-8")
                generated.append("ATS_RESUME")

            # 2. STAR Interview Defense
            interview_path = folder / "STAR_INTERVIEW_DEFENSE.md"
            if not interview_path.exists():
                interview_path.write_text(gen_interview_pack(company_name, role), encoding="utf-8")
                generated.append("STAR_INTERVIEW")

            # 3. 30-60-90 Day Plan
            plan_path = folder / "DAY_30_60_90_PLAN.md"
            if not plan_path.exists():
                plan_path.write_text(gen_plan90(company_name, role), encoding="utf-8")
                generated.append("30-60-90_PLAN")

            # 4. Compensation Negotiation
            negotiate_path = folder / "COMPENSATION_NEGOTIATION.md"
            if not negotiate_path.exists():
                negotiate_path.write_text(gen_negotiation(company_name, ctc), encoding="utf-8")
                generated.append("NEGOTIATION")

            # 5. Master Index (always regenerate)
            index_path = folder / "MASTER_CONQUEST_INDEX.md"
            index_path.write_text(gen_master_index(company_name, role, folder), encoding="utf-8")

            if generated:
                upgraded += 1
                print(f"  [{i:3d}/{total}] [OK] UPGRADED  {display:<55} +{len(generated)} assets ({', '.join(generated)})")
            else:
                skipped += 1
                print(f"  [{i:3d}/{total}] [--] COMPLETE  {display:<55} (all assets present)")

        except Exception as e:
            errors += 1
            print(f"  [{i:3d}/{total}] [ERR] ERROR  {display:<55} ({str(e)[:60]})")

    print(f"\n{'='*72}")
    print(f"  DEPLOYMENT COMPLETE")
    print(f"  Upgraded:  {upgraded} companies")
    print(f"  Skipped:   {skipped} companies (already complete)")
    print(f"  Errors:    {errors}")
    print(f"  Total:     {total} company conquest packs")
    print(f"{'='*72}\n")

    # Generate master summary
    summary_path = BASE_DIR / "OMEGA_BATCH_CONQUEST_SUMMARY.md"
    summary_path.write_text(f"""# OMEGA BATCH CONQUEST ENGINE — DEPLOYMENT SUMMARY
**Executed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Company Packs:** {total}
**Upgraded:** {upgraded}
**Already Complete:** {skipped}
**Errors:** {errors}

## Assets Generated Per Company
Each company folder now contains up to 8 production-ready assets:
1. `APPLICATION_MANIFEST.json` — Company/role/CTC metadata
2. `COVER_LETTER.md` — Executive application pitch letter
3. `DIRECT_OUTREACH_INMAIL.md` — LinkedIn InMail & recruiter outreach
4. `ZERO_RISK_WORK_TRIAL_PROPOSAL.md` — Free trial proposal
5. `ATS_RESUME.md` — 100% ATS-optimized surgical resume
6. `STAR_INTERVIEW_DEFENSE.md` — 360° behavioral Q&A + curveball shields
7. `DAY_30_60_90_PLAN.md` — Strategic onboarding blueprint
8. `COMPENSATION_NEGOTIATION.md` — CTC negotiation scripts
9. `MASTER_CONQUEST_INDEX.md` — Unified asset index

## Candidate
{CANDIDATE['name']} | {CANDIDATE['location']} | {CANDIDATE['phone']}
""", encoding="utf-8")

    print(f"  📄 Summary saved to: {summary_path}")


if __name__ == "__main__":
    process_all_folders()
