"""
generate_all_priority_dossiers.py
==================================
Generates complete 7-file submission-ready dossiers for all top priority
Bengaluru startup and scaleup opportunities for Aditya Mehra (@AdityaMehra007).
"""

import os
import json
import csv

BASE_DIR = "applications_generated"

NEW_TARGETS = {
    "waterscience_founders_office_intern": {
        "job_id": "JOB-063",
        "company": "WaterScience",
        "role": "Founder's Office Intern (Operations & Execution)",
        "location": "In-Office (JP Nagar, Bengaluru)",
        "compensation": "₹15,000 – ₹25,000 / month",
        "fit_score": "98/100",
        "apply_url": "https://in.linkedin.com/jobs/view/founder-s-office-intern-operations-execution-at-waterscience-4474261907",
        "domain": "D2C Hardware, Water Filtration & Retail Supply Chain",
        "founder_focus": "Retail supply chain expansion, D2C warehouse fulfillment operations, inventory turnover, and business performance metrics.",
        "skills_highlight": "D2C logistics, inventory reconciliation, multi-channel retail operations, vendor SLA audits, Form 26AS ₹1.8Cr+ GMV commercial telemetry.",
        "key_initiatives": "Analyze regional distributor stock levels, streamline warehouse dispatch SLAs, monitor channel returns/RTO rates, build daily executive fulfillment dashboards."
    },
    "instawork_operations_management_intern": {
        "job_id": "JOB-042",
        "company": "Instawork",
        "role": "Operations Management Intern",
        "location": "In-Office (Bengaluru Hub)",
        "compensation": "₹25,000 – ₹35,000 / month",
        "fit_score": "97/100",
        "apply_url": "https://in.linkedin.com/jobs/view/operations-management-intern-at-instawork-4411454993",
        "domain": "Flexible Labor Marketplace & On-Demand Staffing Operations",
        "founder_focus": "Managing labor marketplace operations, optimizing shift fill rates, auditing partner service quality, and conducting workflow tracking in SQL/Excel.",
        "skills_highlight": "Two-sided marketplace operations, shift dispatching, partner retention, high-volume real-time triage (Aero India 2025: 1,200+ VIPs handled), SQL/Excel analytics.",
        "key_initiatives": "Audit shift cancellation root causes, design proactive standby staffing queues, optimize fill rates for hospitality and light industrial partners."
    },
    "bitespeed_customer_success_intern": {
        "job_id": "JOB-056",
        "company": "BiteSpeed",
        "role": "Customer Success Intern",
        "location": "In-Office (HSR Layout, Bengaluru)",
        "compensation": "₹20,000 / month",
        "fit_score": "95/100",
        "apply_url": "https://in.linkedin.com/jobs/view/customer-success-intern-at-bitespeed-4476805420",
        "domain": "Conversational Commerce & WhatsApp Marketing SaaS for Shopify",
        "founder_focus": "Onboard Shopify & D2C merchants onto conversational WhatsApp marketing platform; monitor churn signals; run customer product demos.",
        "skills_highlight": "D2C merchant workflows, WhatsApp automation flows, SaaS onboarding cadence, CRM hygiene, empathetic client problem resolution.",
        "key_initiatives": "Standardize merchant time-to-first-campaign from 7 days to 48 hours, monitor weekly message volume health, conduct churn prevention outreach."
    },
    "airtribe_program_manager_intern": {
        "job_id": "JOB-067",
        "company": "Airtribe",
        "role": "Program Manager Internship",
        "location": "In-Office (Koramangala, Bengaluru)",
        "compensation": "₹20,000 – ₹25,000 / month",
        "fit_score": "94/100",
        "apply_url": "https://in.linkedin.com/jobs/view/program-manager-internship-in-bangalore-at-airtribe-4466428284",
        "domain": "Cohort-Based Executive Learning & Tech Community Operations",
        "founder_focus": "Coordinate live executive cohorts, manage guest speakers, drive learner engagement metrics, and run operational feedback loops.",
        "skills_highlight": "Live cohort operations, high-stakes schedule coordination, speaker logistics, community engagement, event management (Aero India, Puma activations).",
        "key_initiatives": "Orchestrate zero-delay live session operations, build student assignment submission trackers, run weekly Net Promoter Score (NPS) analysis."
    },
    "amoga_founders_office_intern": {
        "job_id": "JOB-065",
        "company": "Amoga",
        "role": "Founder's Office Intern",
        "location": "In-Office (Bengaluru)",
        "compensation": "₹15,000 – ₹20,000 / month",
        "fit_score": "93/100",
        "apply_url": "https://in.linkedin.com/jobs/view/founder%E2%80%99s-office-intern-at-amoga-4475609226",
        "domain": "Enterprise Low-Code Work Platform & Business Operating Systems",
        "founder_focus": "Assist founders on product positioning, client discovery workshops, investor update prep, and operational sprint reviews.",
        "skills_highlight": "Enterprise software understanding, autonomous business state machines (built OMEGA & BUSINESS-OS- in Kotlin), pitch deck design, client discovery.",
        "key_initiatives": "Synthesize customer pain points into modular platform capability maps, prepare monthly investor metric updates, run cross-functional sprint checks."
    }
}

def generate_ats_resume(t):
    return f"""# ADITYA MEHRA
**Bengaluru, Karnataka, India | contact.adityamehra007@gmail.com | +91 98450 12345**  
**LinkedIn:** [linkedin.com/in/AdityaMehra007](https://www.linkedin.com/in/AdityaMehra007) | **Portfolio:** [adityamehra007.github.io](https://adityamehra007.github.io) | **GitHub:** [github.com/AdityaMehra007](https://github.com/AdityaMehra007)

---

## PROFESSIONAL SUMMARY
High-velocity strategic operator and BBA International Business graduate (Dayananda Sagar University, Bengaluru, 2026) combining verified commercial track record (**Form 26AS ₹1.80+ Cr GMV handled**; IRDAI regulated advisory) with autonomous software engineering mastery (**19-agent OMEGA swarm, 260-tool MCP Hub, 12 production Kotlin Compose apps**). Proven leadership directing high-stakes defense ground triage at **Aero India 2025** (1,200+ VIPs) and brand activations for **Puma** and **Tata Communications**. Applying for the **{t['role']}** at **{t['company']}** to deliver instant operational leverage, executive dashboarding, and scalable execution.

---

## CORE COMPETENCIES
* **Operations & Strategy:** Executive KPI Dashboards, Supply Chain Logistics, Process Standardization, Milestone Tracking, Vendor SLA Governance
* **Commercial Scale & Analytics:** Financial Modeling, P&L Operations, Gross Margin Analysis, Form 26AS ₹1.8Cr+ GMV Transaction Management, Advanced Excel/Sheets
* **Autonomous AI & Systems:** Workflow Automation, Python / FastAPI, Kotlin 2.0 / Jetpack Compose, Model Context Protocol (MCP), LLM Agent Tooling
* **Cross-Functional Execution:** High-Stakes Ground Triage, Stakeholder Alignment, Client Onboarding, Crisis Resolution, Cross-Border Trade Compliance

---

## PROFESSIONAL EXPERIENCE

### Operations & VIP Protocol Lead | Aero India 2025
*Air Force Station Yelahanka, Bengaluru | Feb 2025*
* Engineered live ground triage protocols across 4 exhibition halls, directing seamless access, movement, and logistics for 1,200+ defense delegates, international VIPs, and exhibitors.
* Resolved 45+ critical protocol, security, and scheduling escalations in real-time with zero schedule delays across 5 intensive operational days.
* Coordinated multi-agency logistical timelines spanning ministry liaisons, civil aviation authorities, and private defense contractors.

### Commercial Operations & Regulated Advisory Associate
*Bengaluru, India | 2024 – 2026*
* Managed commercial transaction operations with cumulative volume exceeding **₹1.80+ Crore GMV** as officially verified on statutory Form 26AS tax statements.
* Maintained 100% regulatory compliance under **IRDAI** standards, advising institutional and retail clients on risk allocation and capital protection.
* Automated client onboarding and portfolio performance reporting, cutting administrative cycle times by 65%.

### Experiential Marketing & Brand Operations Lead | Eventos / Freelance
*Bengaluru, India | 2024 – 2025*
* Spearheaded on-ground operations, attendee throughput, and resource allocation for premier commercial brand activations, including **Puma Run** and **Tata Communications** CXO summits.
* Reconciled inventory, check-in flows, and vendor equipment check-outs for ₹30L+ in technical assets with zero discrepancy.
* Built daily operational debrief dashboards evaluating lead capture integrity and resource utilization.

---

## FLAGSHIP TECHNICAL & OPERATIONAL SYSTEMS (GITHUB SHOWCASE)
* **OMEGA Autonomous AI Architecture ([AdityaMehra007/anti](https://github.com/AdityaMehra007/anti)):** 19-in-1 Omni-Agent Swarm, Bengaluru Startup Radar (1,027 companies, 74 VCs), 260-tool MCP Hub, and 15 enterprise test suites (**176 tests passing 100%**).
* **12 Production Kotlin/Android Apps:** Built clean architecture mobile platforms across Industrial IoT (Aurelion), Financial Modeling (Moneyverse), and Cloud Kitchen KDS (CloudBite).
* **Live Mission Control Cockpits ([adityamehra007.github.io](https://adityamehra007.github.io)):** 15 glassmorphism web cockpits hosted live on GitHub Pages.

---

## EDUCATION
**Bachelor of Business Administration (BBA) – International Business**  
*Dayananda Sagar University (DSU), Bengaluru | 2023 – 2026*  
* Coursework: International Supply Chain Logistics, Global Trade Law, Strategic Management, Managerial Economics, Financial Accounting.

---

## CERTIFICATIONS & RECOGNITION
* **IRDAI Certified Insurance & Regulated Financial Advisor**
* **Advanced Business Analytics & Financial Modeling**
* **Autonomous Multi-Agent AI & MCP Systems Architect**
"""

def generate_cover_letter(t):
    return f"""# COVER LETTER

**To:** The Hiring Team & Founders  
**Company:** {t['company']}  
**Location:** {t['location']}  
**Position:** {t['role']}  
**From:** Aditya Mehra  
**Portfolio:** [adityamehra007.github.io](https://adityamehra007.github.io) | **GitHub:** [github.com/AdityaMehra007](https://github.com/AdityaMehra007)

---

Dear {t['company']} Team,

I am writing to express my strong conviction for the **{t['role']}** position at **{t['company']}**.

Unlike typical applicants who present purely theoretical credentials, my background bridges **statutory commercial operations** and **deep technical systems execution**:

1. **Proven High-Stakes Operational Execution:** At **Aero India 2025** (Air Force Station Yelahanka), I led on-ground triage and VIP protocol across 4 exhibition halls, orchestrating movement and logistics for **1,200+ defense dignitaries and international delegations** with zero schedule failures.
2. **Statutory Financial & Commercial Scale:** I have managed commercial transaction operations exceeding **₹1.80+ Crore GMV** as officially recorded on statutory Form 26AS tax statements, while maintaining 100% compliance as an **IRDAI-regulated advisor**.
3. **Autonomous Systems & Operational Leverage:** I have architected and deployed the **OMEGA Autonomous AI Architecture** ([AdityaMehra007/anti](https://github.com/AdityaMehra007/anti)) featuring 19 specialized subagents, a 260-tool Model Context Protocol (MCP) hub, 12 production Kotlin Android applications, and **15 live mission control cockpits** ([adityamehra007.github.io](https://adityamehra007.github.io)).

### Why {t['company']}?
{t['company']}'s work in **{t['domain']}** demands an operator who thrives under ambiguity, thinks in deterministic systems, and executes relentlessly without requiring hand-holding. Specifically, I am excited to unblock leadership by:
- Taking complete ownership of **{t['key_initiatives']}**.
- Applying structured data analysis in Excel, SQL, and Python to identify operational bottlenecks before they impact customers.
- Bridging technical and business teams to accelerate company milestones.

I am based in Bengaluru and ready to step in immediately to deliver measurable leverage to your team.

Thank you for your consideration, and I look forward to speaking with you.

Sincerely,  
**Aditya Mehra**  
Bengaluru, Karnataka, India  
Email: contact.adityamehra007@gmail.com  
LinkedIn: [linkedin.com/in/AdityaMehra007](https://www.linkedin.com/in/AdityaMehra007)
"""

def generate_outreach_cadence(t):
    return f"""# DIRECT OUTREACH CADENCE — {t['company']}

Target Role: **{t['role']}**  
Portal Link: [{t['apply_url']}]({t['apply_url']})

---

## 🎯 Touch 1: LinkedIn Connection Request Note (300 char limit)

> *"Hi [Founder/Lead], saw your active hiring for {t['role']} at {t['company']}. I'm a BBA International Business grad (DSU Blr) with ₹1.8Cr+ GMV operations proof (Form 26AS) & Aero India 2025 logistics triage lead. Built 15 live AI cockpits (adityamehra007.github.io). Would love to unblock your ops!"*

---

## ✉️ Touch 2: Direct LinkedIn InMail / Founder Email (Day 2)

**Subject:** Unblocking ops for {t['company']} — Aditya Mehra ({t['role']})

Hi [First Name],

I noticed {t['company']}'s recent momentum in {t['domain']} and wanted to reach out directly regarding the **{t['role']}** opening.

Rather than sending a generic resume, here is what I can immediately deliver to unblock leadership:

1. **Relentless Operational Execution:** Led ground protocol and VIP logistics for **1,200+ defense delegates** at **Aero India 2025** with zero schedule escalations.
2. **Commercial & Data Rigor:** Managed **₹1.80+ Cr GMV** in verified commercial operations (statutory Form 26AS backed) with deep spreadsheet and dashboard modeling.
3. **AI & Automation Leverage:** Engineered **15 live interactive mission control cockpits** and a 19-agent autonomous operational engine ([adityamehra007.github.io](https://adityamehra007.github.io)).

I've already prepared a concrete 30-60-90 day impact roadmap targeting **{t['key_initiatives']}**.

Are you free for a 10-minute introductory conversation this week?

Best regards,  
**Aditya Mehra**  
Portfolio: [https://adityamehra007.github.io](https://adityamehra007.github.io)  
GitHub: [https://github.com/AdityaMehra007](https://github.com/AdityaMehra007)  
Bengaluru, India

---

## 🔄 Touch 3: Follow-Up / Quick Value Add (Day 5)

**Subject:** Re: Unblocking ops for {t['company']} — Quick analysis

Hi [First Name],

Following up on my note earlier this week. I spent some time examining {t['company']}'s operational workflows and drafted a brief teardown on how we can optimize **{t['key_initiatives']}** using automated dashboards and structured SLAs.

I would love to share these notes with you or the team. Let me know if you have 5 minutes to connect.

Best,  
Aditya Mehra  
+91 98450 12345
"""

def generate_star_defense(t):
    return f"""# STAR INTERVIEW DEFENSE MATRIX — {t['company']}

Role: **{t['role']}**  
Company: **{t['company']}**

---

### Question 1: "Why {t['company']}, and why the {t['role']}?"
* **Situation:** You're a high-performing graduate evaluating roles across Bengaluru's tech ecosystem.
* **Task:** Demonstrate specific, non-generic conviction for {t['company']}'s mission in {t['domain']}.
* **Action:** Highlight that {t['company']} operates at the exact intersection of operational rigor and high-tempo growth. Point out that the {t['role']} requires an operator who can toggle seamlessly between granular spreadsheet/logistics execution and high-level strategic alignment.
* **Result:** Frame yourself as an apprentice-operator who doesn't need to be micromanaged, but instead acts as a force multiplier for the leadership team.

---

### Question 2: "Tell me about a time you managed high-stakes operations under immense pressure."
* **Situation:** At Aero India 2025 (Air Force Station Yelahanka), managing 4 exhibition halls with 1,200+ international VIPs, defense delegations, and ministry officials.
* **Task:** Maintain 100% adherence to security protocol and VIP movement timelines without bottlenecks.
* **Action:** Deployed dynamic triage protocol, coordinated multi-agency liaisons (Air Force, civil police, private contractors), and personally resolved 45+ security and scheduling escalations on the tarmac.
* **Result:** 5 consecutive days of flawless protocol execution with zero schedule delays, recognized by event leadership.

---

### Question 3: "How do you handle ambiguity and tasks you haven't done before?"
* **Situation:** Needed to build an automated market intelligence radar and multi-agent system from scratch.
* **Task:** Map 1,027 Bengaluru startups and connect 24 Model Context Protocol servers with zero prior boilerplate.
* **Action:** Applied the OMEGA 'Zero Vibe Coding' discipline: broke down problems into test-driven specs, built automated pytest suites (176 tests passing 100%), and validated against real SQLite schemas.
* **Result:** Delivered 15 live glassmorphism cockpits hosted on GitHub Pages that run deterministically.

---

### Question 4: "How will you contribute to: {t['key_initiatives']}?"
* **Situation:** {t['company']} faces continuous operational complexity as transaction/client volume scales.
* **Task:** Introduce operational discipline, eliminate manual errors, and provide leadership with clean data.
* **Action:** I will establish automated daily trackers, audit SLA variances across vendors/distributors, and build self-updating executive dashboards in Google Sheets/Excel.
* **Result:** Immediate visibility for founders, freeing up 15–20 hours of leadership bandwidth each week.
"""

def generate_30_60_90_plan(t):
    return f"""# 30-60-90 DAY STRATEGIC ONBOARDING BLUEPRINT

**Candidate:** Aditya Mehra  
**Role:** {t['role']}  
**Company:** {t['company']}  

---

## 🎯 Days 1 – 30: Absorb, Map & Immediate Quick Wins
* **Objectives:** Build 100% context on {t['company']}'s operational stack, data schemas, vendor/partner relationships, and key metrics.
* **Key Actions:**
  - Shadow all active operational workflows and document standard operating procedures (SOPs).
  - Clean and audit existing operational trackers and data pipelines in Excel/Sheets.
  - Deliver Quick Win: Build a centralized daily metric brief saving leadership 30 minutes every morning.
  - Deliverables: Comprehensive operational friction map + baseline dashboard.

---

## 🚀 Days 31 – 60: Optimize & Accelerate Execution
* **Objectives:** Take full ownership of recurring operational cadence and drive efficiency gains.
* **Key Actions:**
  - Lead execution on **{t['key_initiatives']}**.
  - Automate repetitive manual data exports, status checks, and partner follow-ups using lightweight scripts and AI tooling.
  - Conduct weekly SLA audits and implement preventative error guards.
  - Deliverables: 25% reduction in cycle time for routine fulfillment/client workflows.

---

## 🏆 Days 61 – 90: Scale & Strategic Force Multiplier
* **Objectives:** Operate autonomously as a trusted strategic extension of leadership.
* **Key Actions:**
  - Proactively identify second-order growth bottlenecks and pitch data-backed solutions to founders.
  - Institutionalize automated operational cockpits for cross-departmental visibility.
  - Train incoming interns/associates and prepare quarterly operational planning models.
  - Deliverables: Complete operating manual + fully automated executive reporting suite.
"""

def generate_comp_negotiation(t):
    return f"""# COMPENSATION & NEGOTIATION BENCHMARK

**Role:** {t['role']}  
**Company:** {t['company']}  
**Stated Range:** {t['compensation']}  

---

## 📊 Market Context
* Benchmark for high-caliber Bengaluru startup operations/founder's office interns: ₹15,000 – ₹30,000 / month.
* Full-time PPO conversion target: **₹8.0 LPA – ₹14.0 LPA CTC** upon graduation.

---

## 💎 Value-Anchored Negotiation Strategy
* **The Pivot:** Frame compensation not around student status, but around **instant operational leverage**.
* **Key Anchor:** *"I come with Form 26AS-verified commercial experience (₹1.80+ Cr GMV) and technical systems engineering (12 production apps, 176 automated tests). I don't require training wheels and will unblock leadership from day one."*
* **Target Terms:**
  - Target Fixed Stipend: **Top of published range ({t['compensation']})**.
  - Performance Milestone: Formal review at Day 60 for full-time Pre-Placement Offer (PPO) conversion.
  - Work Mode: Full-time in-office / hybrid alignment.
"""

def main():
    print(f"Generating complete 7-file dossiers for {len(NEW_TARGETS)} priority targets...")
    os.makedirs(BASE_DIR, exist_ok=True)
    
    queue_rows = []
    
    for folder_name, t in NEW_TARGETS.items():
        folder_path = os.path.join(BASE_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        print(f"\nBuilding dossier: {t['company']} ({folder_name})")
        
        # 1. application_manifest.json
        manifest = {
            "job_id": t["job_id"],
            "company": t["company"],
            "role": t["role"],
            "location": t["location"],
            "compensation": t["compensation"],
            "fit_score": t["fit_score"],
            "apply_url": t["apply_url"],
            "status": "READY_FOR_SUBMISSION",
            "candidate": "Aditya Mehra (@AdityaMehra007)",
            "files": [
                "ATS_RESUME.md",
                "cover_letter.md",
                "outreach_cadence.md",
                "STAR_INTERVIEW_DEFENSE.md",
                "DAY_30_60_90_PLAN.md",
                "COMPENSATION_NEGOTIATION.md"
            ]
        }
        with open(os.path.join(folder_path, "application_manifest.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
            
        # 2. ATS_RESUME.md
        with open(os.path.join(folder_path, "ATS_RESUME.md"), "w", encoding="utf-8") as f:
            f.write(generate_ats_resume(t))
            
        # 3. cover_letter.md
        with open(os.path.join(folder_path, "cover_letter.md"), "w", encoding="utf-8") as f:
            f.write(generate_cover_letter(t))
            
        # 4. outreach_cadence.md
        with open(os.path.join(folder_path, "outreach_cadence.md"), "w", encoding="utf-8") as f:
            f.write(generate_outreach_cadence(t))
            
        # 5. STAR_INTERVIEW_DEFENSE.md
        with open(os.path.join(folder_path, "STAR_INTERVIEW_DEFENSE.md"), "w", encoding="utf-8") as f:
            f.write(generate_star_defense(t))
            
        # 6. DAY_30_60_90_PLAN.md
        with open(os.path.join(folder_path, "DAY_30_60_90_PLAN.md"), "w", encoding="utf-8") as f:
            f.write(generate_30_60_90_plan(t))
            
        # 7. COMPENSATION_NEGOTIATION.md
        with open(os.path.join(folder_path, "COMPENSATION_NEGOTIATION.md"), "w", encoding="utf-8") as f:
            f.write(generate_comp_negotiation(t))
            
        print(f"  Successfully wrote 7 files to {folder_path}!")
        
        queue_rows.append({
            "job_id": t["job_id"],
            "company": t["company"],
            "role": t["role"],
            "fit_score": t["fit_score"],
            "compensation": t["compensation"],
            "package_folder": f"applications_generated/{folder_name}",
            "action_required": "Review ATS Resume & Submit to Portal",
            "portal_url": t["apply_url"]
        })
        
    # Append to data/approval_queue.csv
    approval_file = "data/approval_queue.csv"
    existing_job_ids = set()
    if os.path.exists(approval_file):
        with open(approval_file, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for r in reader:
                existing_job_ids.add(r.get("job_id"))
                
    with open(approval_file, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["job_id","company","role","fit_score","compensation","package_folder","action_required","portal_url"])
        for q in queue_rows:
            if q["job_id"] not in existing_job_ids:
                writer.writerow(q)
                print(f"  Added {q['job_id']} ({q['company']}) to data/approval_queue.csv")

    print("\nAll priority dossiers created and staged in approval queue successfully!")

if __name__ == "__main__":
    main()
