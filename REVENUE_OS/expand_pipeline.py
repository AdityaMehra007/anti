import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from REVENUE_OS.database.db import get_db
from REVENUE_OS.leads.lead_engine import LeadEngine
from REVENUE_OS.crm.crm_pipeline import CRMPipeline

def expand():
    db = get_db()
    lead_engine = LeadEngine(db=db)
    crm = CRMPipeline(db=db)

    new_accounts = [
        {
            "id": "EXP-010",
            "company": "Delhivery",
            "website": "https://delhivery.com",
            "industry": "Express Parcel & Heavy Freight Logistics",
            "geography": "Bengaluru / Gurugram, India",
            "company_size": "5000+",
            "contact_name": "VP Enterprise Operations",
            "contact_role": "Head of Express Logistics",
            "contact_email": "ops-partners@delhivery.com",
            "contact_url": "https://linkedin.com/company/delhivery",
            "buying_trigger": "Pan-India freight SLA and automated vendor billing reconciliation mandate",
            "source": "Corporate Filings & Public Job Postings",
            "icp_fit_score": 9.5,
            "pain_score": 9.0,
            "trigger_score": 9.0,
            "ability_to_pay_score": 9.5,
            "urgency_score": 8.0,
            "reachability_score": 8.5,
            "deal_name": "Delhivery Enterprise Freight SLA Reconciliation Retainer",
            "deal_value_inr": 60000.0,
            "stage": "DISCOVERY"
        },
        {
            "id": "EXP-011",
            "company": "Razorpay",
            "website": "https://razorpay.com",
            "industry": "FinTech & Payments Infrastructure",
            "geography": "Bengaluru (Koramangala), India",
            "company_size": "2500+",
            "contact_name": "Director of Merchant Operations",
            "contact_role": "Director of Merchant Experience",
            "contact_email": "merchant-ops@razorpay.com",
            "contact_url": "https://linkedin.com/company/razorpay",
            "buying_trigger": "High-velocity merchant onboarding compliance and chargeback reconciliation",
            "source": "FinTech Ecosystem Directory",
            "icp_fit_score": 9.5,
            "pain_score": 8.5,
            "trigger_score": 9.0,
            "ability_to_pay_score": 9.5,
            "urgency_score": 8.5,
            "reachability_score": 8.5,
            "deal_name": "Razorpay Merchant Compliance & Risk Intelligence Retainer",
            "deal_value_inr": 70000.0,
            "stage": "PROPOSAL"
        },
        {
            "id": "EXP-012",
            "company": "Hasura",
            "website": "https://hasura.io",
            "industry": "Developer Infrastructure & GraphQL Engine",
            "geography": "Bengaluru / Remote",
            "company_size": "200-500",
            "contact_name": "Head of APAC Commercial Growth",
            "contact_role": "VP Commercial Sales",
            "contact_email": "commercial@hasura.io",
            "contact_url": "https://linkedin.com/company/hasura",
            "buying_trigger": "Scaling enterprise data API governance across BFSI and Healthcare",
            "source": "TechCrunch & LinkedIn Signal",
            "icp_fit_score": 9.0,
            "pain_score": 8.5,
            "trigger_score": 8.5,
            "ability_to_pay_score": 9.0,
            "urgency_score": 8.0,
            "reachability_score": 8.5,
            "deal_name": "Hasura APAC Enterprise Account Intelligence Retainer",
            "deal_value_inr": 55000.0,
            "stage": "DISCOVERY"
        },
        {
            "id": "EXP-013",
            "company": "SigNoz",
            "website": "https://signoz.io",
            "industry": "Open-Source APM & Observability",
            "geography": "Bengaluru / Global Remote",
            "company_size": "50-200",
            "contact_name": "Head of Growth",
            "contact_role": "Head of Growth & DevRel",
            "contact_email": "growth@signoz.io",
            "contact_url": "https://linkedin.com/company/signoz",
            "buying_trigger": "Accelerating developer self-serve conversions to enterprise cloud contracts",
            "source": "GitHub Trending & Y-Combinator Directory",
            "icp_fit_score": 9.0,
            "pain_score": 9.0,
            "trigger_score": 8.5,
            "ability_to_pay_score": 8.5,
            "urgency_score": 8.0,
            "reachability_score": 9.0,
            "deal_name": "SigNoz Enterprise APM Outbound Lead Engine",
            "deal_value_inr": 40000.0,
            "stage": "QUALIFIED"
        },
        {
            "id": "EXP-014",
            "company": "KreditBee",
            "website": "https://kreditbee.in",
            "industry": "FinTech & Digital Lending",
            "geography": "Bengaluru (HSR Layout), India",
            "company_size": "1000-2500",
            "contact_name": "VP Operational Risk",
            "contact_role": "Head of Vendor & Tech Risk",
            "contact_email": "procurement-risk@kreditbee.in",
            "contact_url": "https://linkedin.com/company/kreditbee",
            "buying_trigger": "RBI compliance audit on digital lending partner SLA management",
            "source": "Indian FinTech Regulatory Tracker",
            "icp_fit_score": 8.5,
            "pain_score": 9.0,
            "trigger_score": 9.0,
            "ability_to_pay_score": 9.0,
            "urgency_score": 8.5,
            "reachability_score": 8.0,
            "deal_name": "KreditBee Vendor SLA & Regulatory Audit Retainer",
            "deal_value_inr": 50000.0,
            "stage": "DISCOVERY"
        },
        {
            "id": "EXP-015",
            "company": "Groww",
            "website": "https://groww.in",
            "industry": "WealthTech & Stock Broking",
            "geography": "Bengaluru (Outer Ring Road), India",
            "company_size": "2000+",
            "contact_name": "Head of Regulatory Operations",
            "contact_role": "VP Operations",
            "contact_email": "reg-ops@groww.in",
            "contact_url": "https://linkedin.com/company/groww-in",
            "buying_trigger": "SEBI compliance automation on trade reconciliations and vendor telemetry",
            "source": "LinkedIn Talent Intelligence",
            "icp_fit_score": 9.0,
            "pain_score": 8.5,
            "trigger_score": 8.5,
            "ability_to_pay_score": 9.5,
            "urgency_score": 8.0,
            "reachability_score": 8.0,
            "deal_name": "Groww Trade Reconciliation & Vendor Telemetry Retainer",
            "deal_value_inr": 65000.0,
            "stage": "QUALIFIED"
        },
        {
            "id": "EXP-016",
            "company": "Euler Motors",
            "website": "https://eulermotors.com",
            "industry": "Commercial Electric 3-Wheeler Logistics",
            "geography": "Bengaluru / Delhi NCR",
            "company_size": "500-1000",
            "contact_name": "Head of Commercial Fleet BD",
            "contact_role": "Director Commercial Partnerships",
            "contact_email": "fleet-partners@eulermotors.com",
            "contact_url": "https://linkedin.com/company/euler-motors",
            "buying_trigger": "Aggressive expansion into South Indian 3PL fleet deployment",
            "source": "EV Industry India Monitor",
            "icp_fit_score": 8.5,
            "pain_score": 8.5,
            "trigger_score": 9.0,
            "ability_to_pay_score": 8.5,
            "urgency_score": 8.5,
            "reachability_score": 8.5,
            "deal_name": "Euler Motors South India Fleet Outbound Retainer",
            "deal_value_inr": 35000.0,
            "stage": "DISCOVERY"
        },
        {
            "id": "EXP-017",
            "company": "Licious",
            "website": "https://licious.in",
            "industry": "D2C Cold Chain Food & Fresh Meat",
            "geography": "Bengaluru (Marathahalli), India",
            "company_size": "2000+",
            "contact_name": "Head of Cold Chain Logistics",
            "contact_role": "VP Supply Chain",
            "contact_email": "coldchain-ops@licious.in",
            "contact_url": "https://linkedin.com/company/licious",
            "buying_trigger": "Cold chain vendor SLA monitoring and farm-to-fork temperature audit",
            "source": "Retail & D2C Supply Chain News",
            "icp_fit_score": 8.5,
            "pain_score": 9.0,
            "trigger_score": 8.5,
            "ability_to_pay_score": 9.0,
            "urgency_score": 8.0,
            "reachability_score": 8.0,
            "deal_name": "Licious Cold Chain Vendor SLA Audit Retainer",
            "deal_value_inr": 45000.0,
            "stage": "DISCOVERY"
        },
        {
            "id": "EXP-018",
            "company": "Swiggy Instamart Ops",
            "website": "https://swiggy.com",
            "industry": "Quick Commerce Dark Store Operations",
            "geography": "Bengaluru (Bellandur), India",
            "company_size": "5000+",
            "contact_name": "Director Dark Store Procurement",
            "contact_role": "Director of Supply Operations",
            "contact_email": "instamart-vendor@swiggy.in",
            "contact_url": "https://linkedin.com/company/swiggy-in",
            "buying_trigger": "Scaling 10-minute dark store vendor reconciliation and FMCG stock accuracy",
            "source": "Bangalore Tech Park Intelligence",
            "icp_fit_score": 9.5,
            "pain_score": 9.5,
            "trigger_score": 9.0,
            "ability_to_pay_score": 9.5,
            "urgency_score": 9.0,
            "reachability_score": 8.0,
            "deal_name": "Swiggy Instamart Dark Store Vendor SLA Retainer",
            "deal_value_inr": 55000.0,
            "stage": "PROPOSAL"
        },
        {
            "id": "EXP-019",
            "company": "Dunzo Digital",
            "website": "https://dunzo.com",
            "industry": "Hyperlocal B2B Delivery Logistics",
            "geography": "Bengaluru (Indiranagar), India",
            "company_size": "500-1000",
            "contact_name": "Commercial Logistics Lead",
            "contact_role": "Lead B2B Deliveries",
            "contact_email": "b2b-ops@dunzo.in",
            "contact_url": "https://linkedin.com/company/dunzo-in",
            "buying_trigger": "B2B merchant delivery contract renegotiation and margin optimization",
            "source": "Bangalore Startup Directory",
            "icp_fit_score": 8.5,
            "pain_score": 9.0,
            "trigger_score": 8.5,
            "ability_to_pay_score": 8.0,
            "urgency_score": 8.0,
            "reachability_score": 8.5,
            "deal_name": "Dunzo B2B Merchant Contract SLA Retainer",
            "deal_value_inr": 35000.0,
            "stage": "QUALIFIED"
        }
    ]

    print("Ingesting 10 High-Fit Enterprise Targets into REVENUE OS...")
    for acc in new_accounts:
        lid = lead_engine.ingest_lead(acc)
        did = crm.create_deal(
            lead_id=lid,
            deal_name=acc["deal_name"],
            deal_value_inr=acc["deal_value_inr"],
            stage=acc["stage"]
        )
        print(f"  ✓ {acc['company']:<24} | Lead: {lid} | Deal: {did} (₹{acc['deal_value_inr']:,.0f})")

    summary = crm.get_pipeline_summary()
    print("-" * 60)
    print(f"Total Pipeline:    ₹{summary['total_pipeline_inr']:,.0f}")
    print(f"Weighted Pipeline: ₹{summary['weighted_pipeline_inr']:,.0f}")
    print(f"Total Deals:       {summary['deal_count']}")

if __name__ == "__main__":
    expand()
