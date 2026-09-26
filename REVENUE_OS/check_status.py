"""Quick DB status check."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from REVENUE_OS.database.db import get_db

db = get_db()
print("=" * 50)
print("REVENUE OS — DATABASE STATUS")
print("=" * 50)
opps = db.get_opportunities()
print(f"Opportunities: {len(opps)}")
leads = db.get_leads()
print(f"Leads:         {len(leads)}")
deals = db.get_deals()
print(f"Deals:         {len(deals)}")
pending = db.get_pending_approvals()
print(f"Pending Approvals: {len(pending)}")
for a in pending:
    print(f"  → {a['title']}")
    print(f"    Upside: {a.get('upside', 'N/A')}")
print()

# Pipeline summary
from REVENUE_OS.crm.crm_pipeline import CRMPipeline
crm = CRMPipeline(db)
summary = crm.pipeline_summary()
print(f"Pipeline Total:    ₹{summary['total_pipeline']:,.0f}")
print(f"Pipeline Weighted: ₹{summary['weighted_pipeline']:,.0f}")
print(f"Qualified Leads:   {summary['qualified_count']}")
print()

# Revenue health
from REVENUE_OS.revenue.revenue_health import RevenueHealthCalculator
health = RevenueHealthCalculator()
score = health.calculate({
    "mrr": 0,
    "mrr_prev": 0,
    "cac": 0,
    "ltv": 35000,
    "pipeline_value": summary["total_pipeline"],
    "pipeline_weighted": summary["weighted_pipeline"],
    "churn_rate": 0,
    "nps": 0,
    "active_experiments": 1,
    "deals_in_pipeline": len(deals),
    "revenue_streams": 1,
})
print(f"Revenue Health Score: {score}/100")
print("=" * 50)
