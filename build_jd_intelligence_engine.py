#!/usr/bin/env python3
"""
BUILD BENGALURU APEX JD & INTERVIEW DEFENSE MASTER ENGINE
Analyzes, standardizes, and stores detailed Job Descriptions (JDs),
ATS keyword matrices, day-in-the-life workflows, and STAR interview defense
models across all 6 core role archetypes in Bengaluru.
"""
import os
import sys
import json
import sqlite3
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"e:\anti")
DB_PATH = ROOT / "BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite"
OUT_JSON = ROOT / "data" / "BENGALURU_MASTER_JD_INTELLIGENCE.json"
OUT_MD = ROOT / "BENGALURU_APEX_JD_AND_INTERVIEW_DEFENSE_MASTER.md"

JD_INTELLIGENCE = [
    {
        "archetype_id": "JD-ARCH-001",
        "role_title": "Founder's Office Associate / Chief of Staff Associate",
        "target_companies": ["CRED", "Zepto", "Ather Energy", "Razorpay", "Swiggy", "Navi", "PremjiInvest", "Catamaran Ventures"],
        "target_salary_bracket": "₹10.0L - ₹18.0L LPA",
        "summary": "Acts as the direct operational shadow and high-bandwidth force multiplier to the Founder/CEO. Owns end-to-end execution of cross-functional strategic projects, eliminates operational bottlenecks, and manages business cadence.",
        "daily_responsibilities": [
            "Shadow Founder/CEO on high-priority cross-functional fires, weekly business reviews (WBRs), and operational war rooms.",
            "Build automated operational dashboards tracking unit economics, dark store / city turnaround SLAs, and cash reconciliation.",
            "Lead sprint execution across operations, marketing, product, and vendor partnerships with zero supervision.",
            "Draft board updates, executive memos, and operational problem statements for investor review."
        ],
        "ats_keywords_95_plus": [
            "Founder's Office", "Chief of Staff", "Operational Excellence", "Cross-functional Leadership",
            "SOP Enforcement", "Root-Cause Analysis", "Data-driven Decision Making", "Vendor SLA Governance",
            "High-Stress Triage", "Sprint Planning", "Unit Economics", "Workflow Automation"
        ],
        "star_interview_defense": {
            "question": "Tell me about a time you had to manage an unpredictable crisis with high operational stakes and no direct supervision.",
            "situation": "At AERO India 2025 (Yelahanka Air Force Base), our zone faced an unexpected surge of 50,000+ attendees during active VIP flight-line displays, causing a severe crowd bottleneck at Gate 4 and delaying official delegations.",
            "task": "As Ground Operations Lead, I had to immediately re-route crowd density, coordinate with military security liaisons, and ensure zero safety breaches without disrupting flight-line schedules.",
            "action": "Within 7 minutes, I established a secondary exit corridor, re-deployed 18 security marshals to bottleneck pinch points, and coordinated live megaphone directional triage while maintaining continuous radio protocol with air base command.",
            "result": "Cleared the Gate 4 bottleneck in under 22 minutes, restored VIP protocol flow with zero security non-conformances, and maintained a 100% safety record across the 5-day defense aerospace expo."
        }
    },
    {
        "archetype_id": "JD-ARCH-002",
        "role_title": "Global Business Operations Analyst / BizOps Specialist",
        "target_companies": ["Google India", "Microsoft India", "Amazon", "Postman", "BrowserStack", "Meta", "Walmart Global Tech"],
        "target_salary_bracket": "₹9.0L - ₹14.5L LPA",
        "summary": "Drives operational scalability, cross-border commercial contracts, partner SLA tracking, and process optimization within global capability centers and enterprise software unicorns.",
        "daily_responsibilities": [
            "Monitor enterprise partner SLA metrics, contract renewal triggers, and vendor performance handoffs.",
            "Analyze operational telemetry, identify workflow bottlenecks, and synthesize executive business requirement documents (BRDs).",
            "Standardize standard operating procedures (SOPs) across global cross-functional teams in North America, EMEA, and APAC.",
            "Automate repetitive weekly status reporting using Python, SQL, and advanced spreadsheet modeling."
        ],
        "ats_keywords_95_plus": [
            "Business Operations", "BizOps", "Process Optimization", "SLA Governance", "BRD Authoring",
            "Cross-border Workflows", "Telemetry Analysis", "Commercial Contracts", "Vendor Management",
            "SQL Data Modeling", "Continuous Improvement", "Workflow Automation"
        ],
        "star_interview_defense": {
            "question": "How do you evaluate and optimize a broken or inefficient business workflow?",
            "situation": "At Instawork AI operations, our data annotation and review pipeline was experiencing a 15% verification lag due to manual multi-tab validation overhead.",
            "task": "I was tasked with diagnosing the latency root cause and designing an automated quality review protocol to reach a 99%+ accuracy standard.",
            "action": "I mapped the end-to-end data lifecycle, identified redundant validation touchpoints, created standardized automated prompt-check scripts, and instituted a daily quality threshold scorecard.",
            "result": "Reduced status reconciliation time by 25%, eliminated repetitive multi-tab verification steps, and achieved a certified 99.2% QA benchmark score across 5,000+ data operations."
        }
    },
    {
        "archetype_id": "JD-ARCH-003",
        "role_title": "Supply Chain Operations Analyst / Logistics Governance Lead",
        "target_companies": ["Walmart Global Tech", "Target in India", "Cisco Systems", "Dell Technologies", "Hindustan Unilever", "Puma Sports India", "Boeing India", "Tesco HSC"],
        "target_salary_bracket": "₹7.5L - ₹11.5L LPA",
        "summary": "Manages end-to-end supply chain logistics, inventory buffer reconciliation, freight vendor SLA tracking, and customs compliance to guarantee 100% on-time milestone delivery.",
        "daily_responsibilities": [
            "Audit vendor purchase orders, delivery manifests, and fulfillment SLAs across regional distribution hubs.",
            "Calculate landed cost models, demurrage risk, shipping tariffs, and Incoterms 2020 transfer-of-risk terms.",
            "Coordinate physical inventory counts, identify stock shrinkage points, and enforce supplier contract penalty clauses.",
            "Liaise with 3PL freight forwarders, ocean carriers, and airport cargo customs clearing agents."
        ],
        "ats_keywords_95_plus": [
            "Supply Chain Management (SCM)", "Logistics Operations", "Incoterms 2020", "Landed Cost Modeling",
            "Vendor SLA Compliance", "Demurrage Auditing", "Bill of Lading", "Purchase Order Reconciliation",
            "Inventory Buffer", "3PL Freight Forwarding", "Zero-Shrinkage Logistics"
        ],
        "star_interview_defense": {
            "question": "Give an example of how you enforced supplier accountability or resolved an inventory fulfillment discrepancy.",
            "situation": "During the Puma Sports India brand activation and retail pop-up rollout in Bengaluru, an external logistics vendor delivered merchandise with an 8% item mismatch against the approved purchase order manifest 4 hours before launch.",
            "task": "As Ground Logistics Lead, I had to reconcile the physical inventory, establish custody accountability, and prevent any stock-out during the retail event.",
            "action": "I immediately initiated a serial-number barcode audit, invoked the pre-signed vendor SLA clause requiring emergency replenishment within 120 minutes at vendor expense, and adjusted floor merchandising allocation.",
            "result": "Received the rectified replacement inventory 90 minutes before opening, delivered 100% on-time launch with zero retail shrinkage, and recovered ₹45,000 in contractual penalty credits."
        }
    },
    {
        "archetype_id": "JD-ARCH-004",
        "role_title": "Global Trade Finance & Clearance Analyst",
        "target_companies": ["Goldman Sachs", "JPMorgan Chase", "HSBC EDPI", "Barclays GSC", "Standard Chartered GBS", "A.P. Moller - Maersk", "DHL Global Forwarding"],
        "target_salary_bracket": "₹7.2L - ₹13.0L LPA",
        "summary": "Executes international trade finance settlements, Letter of Credit (LC) scrutiny under UCP 600 rules, cross-border clearing compliance, and post-trade FX settlement audits.",
        "daily_responsibilities": [
            "Audit cross-border trade documentation, commercial invoices, certificates of origin, and bills of lading.",
            "Scrutinize Letters of Credit (LCs) for discrepancies under ICC UCP 600 and ISBP guidelines.",
            "Reconcile SWIFT MT700/MT710 financial messaging and cross-border currency clearing balances.",
            "Enforce strict Anti-Money Laundering (AML) and trade-based money laundering regulatory risk controls."
        ],
        "ats_keywords_95_plus": [
            "Trade Finance", "UCP 600", "Letters of Credit (LC)", "Bill of Lading", "Documentary Collections",
            "Cross-border Settlement", "SWIFT MT700", "Customs Clearance", "Incoterms", "Trade Compliance",
            "FX Trade Clearance", "Financial Reconciliation"
        ],
        "star_interview_defense": {
            "question": "How does your academic training in International Business prepare you for high-stakes trade operations?",
            "situation": "During my BBA in International Business at Dayananda Sagar University, our advanced EXIM lab evaluated complex documentary credit disputes and cross-border payment risks under UCP 600 rules.",
            "task": "I had to analyze multi-jurisdictional shipping documents where the bill of lading description conflicted with the LC terms, risking non-payment and maritime demurrage.",
            "action": "Applying strict UCP 600 Article 14 standards, I cross-referenced the transport documents against the insurance certificate and commercial invoice, identified the discrepancy, and structured a compliant amendment.",
            "result": "Demonstrated full operational command of international commercial documentation, eliminating financial exposure and securing top distinction in trade finance practicals."
        }
    },
    {
        "archetype_id": "JD-ARCH-005",
        "role_title": "AI Compute & Data Operations Associate",
        "target_companies": ["NVIDIA Graphics India", "Krutrim AI", "Google DeepMind", "Microsoft Research India", "Sarvam AI", "Instawork"],
        "target_salary_bracket": "₹9.0L - ₹15.0L LPA",
        "summary": "Operates at the intersection of AI platforms and data pipelines. Coordinates model evaluation datasets, ensures 99%+ quality assurance benchmarks, and audits GPU/compute workflow pipelines.",
        "daily_responsibilities": [
            "Curate, clean, and validate massive multi-modal datasets for LLM evaluation and domain-specific fine-tuning.",
            "Audit annotation quality scores, train human-in-the-loop reviewers, and maintain 99%+ accuracy benchmarks.",
            "Design prompt-testing harnesses, evaluate hallucination rates, and structure automated regression test cases.",
            "Track compute cluster allocation schedules and operational throughput metrics for research engineers."
        ],
        "ats_keywords_95_plus": [
            "AI Operations", "LLM Evaluation", "Data Quality Assurance", "Prompt Engineering", "Dataset Curation",
            "Human-in-the-loop (HITL)", "Regression Testing", "Hallucination Auditing", "Workflow Automation",
            "Compute Scheduling", "Instawork AI QA"
        ],
        "star_interview_defense": {
            "question": "Describe your experience ensuring high accuracy and rigor in AI-driven data pipelines.",
            "situation": "At Instawork AI operations, maintaining flawless data integrity was paramount for enterprise client deployments.",
            "task": "I had to review and benchmark complex, structured datasets to ensure they satisfied strict production reliability standards.",
            "action": "I developed automated verification checklists, conducted rigorous edge-case audits, and leveraged advanced prompt formatting to validate structured outputs against ground truth.",
            "result": "Consistently maintained a verified 99%+ quality rating across all batches, recognized as a top-tier operational contributor."
        }
    },
    {
        "archetype_id": "JD-ARCH-006",
        "role_title": "Risk Advisory & Operational Governance Analyst",
        "target_companies": ["Deloitte US-India", "EY GDS", "PwC SDC", "KPMG KGS", "Swiss Re GBS"],
        "target_salary_bracket": "₹7.2L - ₹11.5L LPA",
        "summary": "Performs enterprise operational audits, internal control reviews, supply chain compliance checks, and governance frameworks for Fortune 500 global clients.",
        "daily_responsibilities": [
            "Execute control testing and operational walkthroughs to identify process failure points.",
            "Audit commercial vendor contracts for SLA conformity, pricing leakage, and regulatory non-compliance.",
            "Synthesize audit workpapers, risk heatmaps, and executive remediation recommendations.",
            "Track global client milestone deliverables across multi-tenant delivery environments."
        ],
        "ats_keywords_95_plus": [
            "Risk Advisory", "Operational Governance", "Internal Controls", "Process Walkthrough",
            "Contract Auditing", "Compliance Testing", "SLA Verification", "Enterprise Risk Management",
            "Audit Workpapers", "Remediation Planning", "Global Delivery Services"
        ],
        "star_interview_defense": {
            "question": "How do you maintain high attention to detail when auditing complex enterprise contracts or data?",
            "situation": "While reviewing vendor agreements for major experiential activations (including Tata Communications and Puma India), multiple rate-card discrepancies and unclear penalty clauses were buried in schedule annexures.",
            "task": "I needed to audit 12 vendor rate cards to eliminate commercial leakage and align all terms with standardized service level agreements.",
            "action": "I built a centralized cost-reconciliation matrix, cross-checked invoice rates against contracted milestones, and flagged ambiguity in overtime and logistics surcharges.",
            "result": "Eliminated 100% of billing variance, saved approximately 18% in unanticipated surcharge claims, and established a repeatable vendor audit playbook."
        }
    }
]

def build():
    print("=" * 80)
    print("   BUILDING BENGALURU APEX JD & INTERVIEW DEFENSE MASTER")
    print("=" * 80)
    
    # 1. Save JSON
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(JD_INTELLIGENCE, f, indent=2)
    print(f"-> Saved Structured JD Intelligence: {OUT_JSON}")
    
    # 2. Write Markdown Master Document
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# BENGALURU APEX JOB DESCRIPTION & INTERVIEW DEFENSE MASTER\n\n")
        f.write("> **Candidate:** Aditya Mehra | BBA International Business (DSU '26) | Bengaluru\n")
        f.write("> **Scope:** Deep-dive analysis of all 6 target role archetypes across Bengaluru's Top 50 Employers\n")
        f.write("> **Purpose:** 100% ATS Keyword Optimization + Proven STAR-Method Behavioral Interview Defense\n\n---\n\n")
        
        for jd in JD_INTELLIGENCE:
            f.write(f"## {jd['archetype_id']}: {jd['role_title']}\n\n")
            f.write(f"- **Target Companies:** {', '.join(jd['target_companies'])}\n")
            f.write(f"- **Compensation Bracket:** **{jd['target_salary_bracket']}**\n")
            f.write(f"- **Executive Summary:** {jd['summary']}\n\n")
            
            f.write("### 1. Daily Core Responsibilities (What You Do 9 AM – 6 PM)\n")
            for r in jd['daily_responsibilities']:
                f.write(f"- {r}\n")
            f.write("\n")
            
            f.write("### 2. High-Scoring ATS Keywords (95%+ Match Rate on Workday / Greenhouse)\n")
            f.write(f"`{'` • `'.join(jd['ats_keywords_95_plus'])}`\n\n")
            
            f.write("### 3. STAR-Method Behavioral Interview Defense Script\n")
            star = jd['star_interview_defense']
            f.write(f"> **Core Question:** *\"{star['question']}\"*\n>\n")
            f.write(f"> • **Situation:** {star['situation']}\n>\n")
            f.write(f"> • **Task:** {star['task']}\n>\n")
            f.write(f"> • **Action:** {star['action']}\n>\n")
            f.write(f"> • **Result:** **{star['result']}**\n\n---\n\n")
            
    print(f"-> Saved Markdown Playbook: {OUT_MD}")
    
    # 3. Ingest into SQLite Database
    if DB_PATH.exists():
        conn = sqlite3.connect(str(DB_PATH))
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS job_descriptions_master (
            archetype_id TEXT PRIMARY KEY,
            role_title TEXT,
            target_companies TEXT,
            salary_bracket TEXT,
            summary TEXT,
            daily_responsibilities TEXT,
            ats_keywords TEXT,
            star_question TEXT,
            star_defense TEXT
        )
        """)
        for jd in JD_INTELLIGENCE:
            cur.execute("""
            INSERT OR REPLACE INTO job_descriptions_master VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                jd["archetype_id"],
                jd["role_title"],
                ", ".join(jd["target_companies"]),
                jd["target_salary_bracket"],
                jd["summary"],
                "\n".join(jd["daily_responsibilities"]),
                ", ".join(jd["ats_keywords_95_plus"]),
                jd["star_interview_defense"]["question"],
                json.dumps(jd["star_interview_defense"])
            ))
            # Also add to FTS5 table
            cur.execute("""
            INSERT INTO master_search_fts VALUES ('job_descriptions_master', ?, ?, ?, ?, ?, ?, ?)
            """, (
                jd["role_title"],
                jd["archetype_id"],
                jd["target_salary_bracket"],
                "",
                "Bengaluru",
                jd["role_title"],
                ", ".join(jd["ats_keywords_95_plus"])
            ))
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM job_descriptions_master")
        total_jds = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM master_search_fts")
        total_fts = cur.fetchone()[0]
        print(f"-> Ingested {total_jds} Master JDs into {DB_PATH}")
        print(f"-> Updated Total FTS5 Search Entities: {total_fts}")
        conn.close()

if __name__ == "__main__":
    build()
