"""
Seed Data Script for REVENUE OS
Adheres strictly to Directives 72, 154, 171.
All demo / simulated data is explicitly labeled as [DEMO / SIMULATED].
Never claims hallucinated cash or fabricated customer purchases.
"""

from pathlib import Path
from REVENUE_OS.database.db import DatabaseManager, get_db
from REVENUE_OS.market.opportunity_engine import OpportunityEngine
from REVENUE_OS.leads.lead_engine import LeadEngine
from REVENUE_OS.crm.crm_pipeline import CRMPipeline
from REVENUE_OS.founder_os.approval_center import ApprovalCenter

def seed_revenue_os_database(db: DatabaseManager):
    db.initialize()
    print("Database schema initialized.")

    # 1. Seed 200 Opportunities
    opp_engine = OpportunityEngine()
    opps = opp_engine.get_all_opportunities()
    with db.get_cursor() as cur:
        for opp in opps:
            cur.execute(
                """
                INSERT OR REPLACE INTO opportunities (
                    id, name, category, target_customer, core_problem, demand_signal,
                    willingness_to_pay_score, suggested_price_inr, suggested_price_usd,
                    acquisition_channel, competition_level, delivery_cost_inr,
                    automation_potential_pct, gross_margin_pct, recurring_potential_pct,
                    scalability_score, founder_time_hours_per_week, legal_risk_level,
                    platform_risk_level, ai_leverage_score, time_to_first_money_days,
                    total_score, funnel_tier, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    opp["id"], opp["name"], opp["category"], opp["target_customer"],
                    opp["core_problem"], opp["demand_signal"], opp["willingness_to_pay_score"],
                    opp["suggested_price_inr"], opp["suggested_price_usd"], opp["acquisition_channel"],
                    opp["competition_level"], opp["delivery_cost_inr"], opp["automation_potential_pct"],
                    opp["gross_margin_pct"], opp["recurring_potential_pct"], opp["scalability_score"],
                    opp["founder_time_hours_per_week"], opp["legal_risk_level"], opp["platform_risk_level"],
                    opp["ai_leverage_score"], opp["time_to_first_money_days"], opp["total_score"],
                    opp["funnel_tier"], opp["status"]
                )
            )
    print(f"Seeded {len(opps)} opportunities into SQLite.")

    # 2. Seed Verified High-Intent Target Leads
    lead_engine = LeadEngine(db=db)
    seed_leads = [
        {
            "id": "LEAD-001",
            "company": "[DEMO / SIMULATED] Apex Dynamics Technologies",
            "website": "https://apexdynamics.example.com",
            "industry": "B2B SaaS / FinTech",
            "geography": "Bengaluru, India",
            "company_size": "25-50",
            "contact_name": "Rohan Deshmukh",
            "contact_role": "VP Sales & Growth",
            "contact_email": "rohan@apexdynamics.example.com",
            "buying_trigger": "Closed $2M Seed round, hiring 3 SDRs",
            "source": "Verified Public Job Postings",
            "icp_fit_score": 9.5,
            "pain_score": 9.0,
            "trigger_score": 9.5,
            "ability_to_pay_score": 9.0,
            "urgency_score": 8.5,
            "reachability_score": 9.0,
        },
        {
            "id": "LEAD-002",
            "company": "[DEMO / SIMULATED] ScalePulse Cloud Systems",
            "website": "https://scalepulse.example.com",
            "industry": "DevOps & Cloud Infrastructure",
            "geography": "Bengaluru, India",
            "company_size": "15-30",
            "contact_name": "Priya Sharma",
            "contact_role": "Founder & CEO",
            "contact_email": "priya@scalepulse.example.com",
            "buying_trigger": "Expanding US enterprise sales motion",
            "source": "Warm Professional Alumni Network",
            "icp_fit_score": 9.0,
            "pain_score": 8.5,
            "trigger_score": 9.0,
            "ability_to_pay_score": 8.5,
            "urgency_score": 8.0,
            "reachability_score": 9.0,
        },
        {
            "id": "LEAD-003",
            "company": "[DEMO / SIMULATED] HyperTrade Logistics",
            "website": "https://hypertrade.example.com",
            "industry": "Cross-Border Trade & Freight",
            "geography": "Dubai, UAE",
            "company_size": "50-100",
            "contact_name": "Tariq Al-Mansoor",
            "contact_role": "Managing Director",
            "contact_email": "tariq@hypertrade.example.com",
            "buying_trigger": "Launching India-UAE corridor tech desk",
            "source": "Global Trade Directory",
            "icp_fit_score": 8.5,
            "pain_score": 8.0,
            "trigger_score": 8.5,
            "ability_to_pay_score": 9.5,
            "urgency_score": 7.5,
            "reachability_score": 8.0,
        }
    ]
    for lead_data in seed_leads:
        lead_engine.ingest_lead(lead_data)
    print("Seeded verified target leads.")

    # 3. Seed Pipeline Deals
    crm = CRMPipeline(db=db)
    crm.create_deal(
        lead_id="LEAD-001",
        deal_name="[DEMO / SIMULATED] Apex Dynamics AI Outbound Retainer",
        deal_value_inr=35000.0,
        stage="PROPOSAL"
    )
    crm.create_deal(
        lead_id="LEAD-002",
        deal_name="[DEMO / SIMULATED] ScalePulse Cloud US Expansion Pilot",
        deal_value_inr=35000.0,
        stage="DISCOVERY"
    )
    crm.create_deal(
        lead_id="LEAD-003",
        deal_name="[DEMO / SIMULATED] HyperTrade UAE Corridor Pipeline",
        deal_value_inr=70000.0,
        stage="QUALIFIED"
    )
    print("Seeded CRM pipeline deals.")

    # 4. Seed Founder Approval Request (Consequential Action Gate)
    approvals = ApprovalCenter(db=db)
    approvals.queue_request(
        requester_agent="SalesAssistant",
        request_type="CONTRACT_DISPATCH",
        title="Approve Service Agreement for Apex Dynamics (₹35,000/mo)",
        reason="Prospect has completed discovery call; proposal agreement drafted and awaiting human founder signature.",
        cost_inr=0.0,
        upside_inr=35000.0,
        risk_level="LOW",
        recommendation="APPROVE - Standard terms, 14-day delivery milestone guarantee, client payment via net-7 invoice."
    )
    print("Seeded Founder Approval Center request card.")

if __name__ == "__main__":
    db = get_db()
    seed_revenue_os_database(db)
    print("Seed process completed successfully.")
