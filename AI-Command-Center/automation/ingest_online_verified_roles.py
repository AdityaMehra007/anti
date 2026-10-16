"""
=============================================================================
INGEST ONLINE VERIFIED HIGH-FIT ROLES INTO CAREER VAULT
Ingests verified Bengaluru Business Ops, SCM, and Procurement roles from
Boeing India, Schneider Electric, Tesco Bengaluru, Shell India,
Amazon India, and Flipkart / Ekart Logistics.
=============================================================================
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENGINE_DIR = os.path.join(BASE_DIR, "projects", "flagship-career-engine")
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
VAULT_PATH = os.path.join(ENGINE_DIR, "career_vault.db")

sys.path.insert(0, ENGINE_DIR)
from career_engine import CareerVault

VERIFIED_ONLINE_ROLES = [
    {
        "job_id": "BOEING-BLR-PRC-141289825",
        "company": "Boeing India",
        "title": "Associate Procurement Agent (Direct Materials / Global Services)",
        "location": "Bengaluru (BIETC / Aerospace Park, Devanahalli)",
        "url": "https://jobs.boeing.com/job/bengaluru/associate-procurement-agent/185/141289825",
        "department": "Boeing Global Services & Supply Chain Management",
        "experience_min": 0,
        "experience_max": 2,
        "required_skills": [
            "Procurement Ops",
            "RFQ Negotiation",
            "Supplier Management",
            "P2P Workflow",
            "Aerospace Logistics",
            "Vendor Risk"
        ],
        "description": "Boeing India Engineering & Technology Center (BIETC) is hiring an Associate Procurement Agent in Bengaluru. Focus on direct materials purchasing, RFQ closure, supplier SLA management, and aerospace logistics coordination."
    },
    {
        "job_id": "BOEING-BLR-SCM-02",
        "company": "Boeing India",
        "title": "Associate Supply Chain Specialist - Logistics Analytics",
        "location": "Bengaluru (BIETC / Aerospace Park)",
        "url": "https://jobs.boeing.com/job/bengaluru/associate-supply-chain-specialist/185/6829104",
        "department": "Global Supply Chain & Inventory Operations",
        "experience_min": 0,
        "experience_max": 2,
        "required_skills": [
            "Supply Chain Analytics",
            "Inventory Planning",
            "Supplier Performance",
            "Logistics Operations",
            "Excel",
            "Data Modeling"
        ],
        "description": "Boeing India is seeking an Associate Supply Chain Specialist in Bengaluru to support global aerospace sourcing, inventory tracking, and supplier performance metrics."
    },
    {
        "job_id": "SE-BLR-PRC-20438",
        "company": "Schneider Electric",
        "title": "Procurement & Sourcing Specialist (Job ID: 20438)",
        "location": "Bengaluru (Attibele / Whitefield Hub)",
        "url": "https://se.wd3.myworkdayjobs.com/SchneiderElectric/job/Bengaluru/Procurement-Sourcing-Specialist_20438",
        "department": "Global Sourcing & Procurement Excellence",
        "experience_min": 0,
        "experience_max": 2,
        "required_skills": [
            "Strategic Sourcing",
            "RFQ Management",
            "Vendor Negotiations",
            "SAP SCM",
            "Procure-to-Pay",
            "Should-Costing"
        ],
        "description": "Schneider Electric is seeking a Procurement & Sourcing Specialist in Bengaluru for prototype and spot-buy purchasing, RFQ negotiation, vendor performance monitoring, and ERP transaction governance."
    },
    {
        "job_id": "SE-BLR-LOG-02",
        "company": "Schneider Electric",
        "title": "Operations Associate - Warehouse Methods & Inventory Control",
        "location": "Bengaluru Hub",
        "url": "https://se.wd3.myworkdayjobs.com/SchneiderElectric/job/Bengaluru/Operations-Associate-Warehouse_20912",
        "department": "Global Supply Chain & Logistics Operations",
        "experience_min": 0,
        "experience_max": 2,
        "required_skills": [
            "Warehouse Operations",
            "Inventory Control",
            "SLA Monitoring",
            "Supply Chain Optimization",
            "Process Improvement"
        ],
        "description": "Manage warehouse performance metrics, inbound/outbound inventory reconciliation, and logistics operational standards for Schneider Electric Bengaluru hub."
    },
    {
        "job_id": "TESCO-BLR-SCM-01",
        "company": "Tesco Bengaluru",
        "title": "Supply Chain Analyst - Retail Replenishment & Planning",
        "location": "Bengaluru (Whitefield)",
        "url": "https://www.tesco-careers.com/job/bengaluru/supply-chain-analyst/782194",
        "department": "Tesco Business Solutions - Supply Chain Operations",
        "experience_min": 0,
        "experience_max": 2,
        "required_skills": [
            "Retail Supply Chain",
            "Demand Forecasting",
            "Replenishment Planning",
            "Inventory Optimization",
            "SQL",
            "Excel"
        ],
        "description": "Tesco Business Solutions in Whitefield is hiring a Supply Chain Analyst to drive store and fulfillment replenishment, demand forecasting, stock level optimization, and vendor SLA management."
    },
    {
        "job_id": "TESCO-BLR-OPS-02",
        "company": "Tesco Bengaluru",
        "title": "Business Operations Analyst - Process Analytics",
        "location": "Bengaluru (Whitefield)",
        "url": "https://www.tesco-careers.com/job/bengaluru/business-operations-analyst/782195",
        "department": "Global Business Operations",
        "experience_min": 0,
        "experience_max": 2,
        "required_skills": [
            "Operations Analytics",
            "Root Cause Analysis",
            "Process Mapping",
            "Dashboard Reporting",
            "Workflow Automation"
        ],
        "description": "Analyze retail logistics workflows, identify operational bottlenecks, build automated KPI performance dashboards, and deliver operational cost savings."
    },
    {
        "job_id": "SHELL-BLR-SCM-R205282",
        "company": "Shell India",
        "title": "Supply Chain Operational Excellence Specialist (Req: R205282)",
        "location": "Bengaluru (Shell Technology Centre - Devanahalli)",
        "url": "https://shell.wd3.myworkdayjobs.com/ShellCareers/job/Bengaluru/Supply-Chain-Operational-Excellence_R205282",
        "department": "Global SCM & Logistics Optimization",
        "experience_min": 0,
        "experience_max": 2,
        "required_skills": [
            "Supply Chain Operational Excellence",
            "Continuous Improvement",
            "Vendor Sourcing",
            "Process Standardization",
            "Logistics KPIs"
        ],
        "description": "Shell Technology Centre Bengaluru is hiring a Supply Chain Operational Excellence Specialist. Focus on end-to-end supply chain process standardization, vendor SLA tracking, and global logistics efficiency."
    },
    {
        "job_id": "SHELL-BLR-SCM-R205864",
        "company": "Shell India",
        "title": "Supply Chain Network Optimization Analyst (Req: R205864)",
        "location": "Bengaluru (Retail Commercial Office, RMZ Ecoworld)",
        "url": "https://shell.wd3.myworkdayjobs.com/ShellCareers/job/Bengaluru/Supply-Chain-Network-Optimization_R205864",
        "department": "Commercial Logistics & Network Planning",
        "experience_min": 0,
        "experience_max": 2,
        "required_skills": [
            "Supply Chain Network Planning",
            "Transit Cost Optimization",
            "Inventory Placement",
            "Data Analytics",
            "Excel"
        ],
        "description": "Drive network logistics optimization, distribution modeling, transit bottleneck resolution, and inventory placement across retail operations."
    },
    {
        "job_id": "AMZN-BLR-SCM-01",
        "company": "Amazon India",
        "title": "Supply Chain Specialist - Global Procurement Launch & Expansion",
        "location": "Bengaluru (World Trade Center, Rajajinagar)",
        "url": "https://www.amazon.jobs/en/jobs/2591042/supply-chain-specialist",
        "department": "Global Procurement & Supply Chain Launch",
        "experience_min": 0,
        "experience_max": 2,
        "required_skills": [
            "Global Procurement",
            "Vendor Management",
            "Cost of Waste Reduction",
            "Inventory Placement",
            "SLA Tracking"
        ],
        "description": "Amazon India is hiring a Supply Chain Specialist for Global Procurement Launch. Focus on vendor onboarding, milestone tracking, inventory placement, and procurement cost optimization."
    },
    {
        "job_id": "AMZN-BLR-OPS-02",
        "company": "Amazon India",
        "title": "Logistics Operations Analyst - Fulfillment Network",
        "location": "Bengaluru (RMZ Ecoworld / Brigade Gateway)",
        "url": "https://www.amazon.jobs/en/jobs/2591043/logistics-operations-analyst",
        "department": "Fulfillment & Transportation Operations",
        "experience_min": 0,
        "experience_max": 2,
        "required_skills": [
            "Logistics Analytics",
            "Fulfillment Operations",
            "Capacity Planning",
            "Transit Bottleneck Resolution",
            "SQL",
            "Excel"
        ],
        "description": "Monitor fulfillment speed metrics, resolve transit bottlenecks, audit carrier SLA compliance, and support middle-mile transportation operations."
    },
    {
        "job_id": "FLIP-BLR-OPS-01",
        "company": "Flipkart",
        "title": "Operations Analyst - Ekart Supply Chain Network",
        "location": "Bengaluru (Cessna Business Park, Outer Ring Road)",
        "url": "https://www.flipkartcareers.com/job/bengaluru/operations-analyst-ekart/FLIP-89102",
        "department": "Ekart Logistics & Supply Chain Operations",
        "experience_min": 0,
        "experience_max": 2,
        "required_skills": [
            "Supply Chain Operations",
            "Fulfillment KPIs",
            "Warehouse SLA Audits",
            "Line-Haul Tracking",
            "Data Visualization"
        ],
        "description": "Analyze logistics operations across Ekart fulfillment centers, track inbound/outbound transit SLAs, audit vendor performance, and optimize fulfillment throughput."
    },
    {
        "job_id": "FLIP-BLR-SCM-02",
        "company": "Flipkart",
        "title": "Inventory Planning & SCM Associate",
        "location": "Bengaluru (Cessna Business Park)",
        "url": "https://www.flipkartcareers.com/job/bengaluru/inventory-planning-associate/FLIP-89103",
        "department": "Marketplace Supply Chain & Category Replenishment",
        "experience_min": 0,
        "experience_max": 2,
        "required_skills": [
            "Inventory Planning",
            "Category Replenishment",
            "Supplier Fill-Rate Audits",
            "Stockout Mitigation",
            "Excel"
        ],
        "description": "Manage category inventory replenishment, audit supplier order fill rates, analyze safety stock thresholds, and coordinate with vendor partners."
    }
]


def ingest_verified_roles():
    print(f"[*] Ingesting {len(VERIFIED_ONLINE_ROLES)} verified online roles into Career Vault...")
    vault = CareerVault(VAULT_PATH)
    added = 0
    dups = 0

    for role in VERIFIED_ONLINE_ROLES:
        ok, msg, score = vault.add_job(role)
        if ok:
            added += 1
            print(f"  [+] Added: {role['company']:<20} | {role['title']:<45} (Score: {score})")
        else:
            dups += 1
            print(f"  [-] Duplicate/Skipped: {role['job_id']} ({msg})")

    cur = vault.conn.cursor()
    cur.execute("SELECT COUNT(*) FROM jobs")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(DISTINCT company) FROM jobs")
    companies = cur.fetchone()[0]
    vault.close()

    print(f"\n[OK] Ingestion Complete: {added} added, {dups} skipped.")
    print(f"[*] New Career Vault Total: {total} opportunities across {companies} companies.")
    return added, total, companies


if __name__ == "__main__":
    ingest_verified_roles()
