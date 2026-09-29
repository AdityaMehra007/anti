"""
Daily Cash Hunter & Realized Profit Engine
Executes daily profit auditing, active pipeline monetization, and automated cash pacing.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# UTF-8 encoding support
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from REVENUE_OS.finance.daily_profit_engine import DailyProfitEngine
from REVENUE_OS.database.db import get_db

def run_daily_cash_hunt():
    db = get_db()
    profit_engine = DailyProfitEngine(db=db)
    
    print("\n" + "=" * 68)
    print("      ANTIGRAVITY DAILY CASH & PROFIT HUNTING ENGINE")
    print("=" * 68)
    
    # 1. Today's Profit & Loss Summary
    summary = profit_engine.get_daily_summary()
    print(f"[*] Date:                 {summary['date']}")
    print(f"[*] Operator:             Aditya Mehra (+91 70034 56624)")
    print(f"[*] Daily Target:         ₹{summary['daily_target_inr']:,.2f} / day")
    print(f"[*] Today's Gross Inflow: ₹{summary['gross_revenue_inr']:,.2f}")
    print(f"[*] Variable Delivery:    ₹{summary['variable_costs_inr']:,.2f}")
    print(f"[+] TODAY'S NET PROFIT:   ₹{summary['net_profit_inr']:,.2f}")
    print(f"[*] Profit Margin:        {summary['profit_margin_pct']}%")
    print(f"[*] Target Attainment:    {summary['target_achievement_pct']}% (Remaining: ₹{summary['target_remaining_inr']:,.2f})")
    
    # 2. Today's Verified Transactions
    txns = profit_engine.get_daily_ledger(limit=10)
    print("\n--- TODAY'S RECOGNIZED CASH TRANSACTIONS ---")
    for t in txns:
        print(f"  [{t['transaction_time']}] {t['client_or_customer'][:22]:<22} | Gross: ₹{t['gross_amount_inr']:>8.2f} | Net: ₹{t['net_profit_inr']:>8.2f} ({t['payment_rail']})")
        
    # 3. High-Yield Pipeline Closures Available Today
    print("\n--- TODAY'S HIGHEST-YIELD DEALS TO CLOSE ---")
    with db.get_cursor() as cur:
        cur.execute("""
            SELECT d.deal_name, d.deal_value_inr, d.stage, d.expected_revenue_inr, l.company
            FROM deals d
            LEFT JOIN leads l ON d.lead_id = l.id
            ORDER BY d.expected_revenue_inr DESC
            LIMIT 5
        """)
        top_deals = cur.fetchall()
        for idx, d in enumerate(top_deals, 1):
            print(f"  {idx}. {d['deal_name']} ({d['company']})")
            print(f"     Value: ₹{d['deal_value_inr']:,.2f} | Stage: {d['stage']} | Weighted: ₹{d['expected_revenue_inr']:,.2f}")
            
    # 4. Immediate Daily Inflow Action Steps
    print("\n--- DAILY PROFIT ACCELERATION ACTIONS ---")
    print("  1. DISPATCH B2B DOSSIERS: 5 tailored outbound dossiers in REVENUE_OS/06_SALES/active_outreach_dossiers/")
    print("  2. SHARE MICRO-SAAS TOOLS: EXIM Calculator (₹999 unlock) & ATS Scanner (₹299 unlock)")
    print("  3. RECEIVE UPI: Scan dynamic QR on Daily Cash Machine dashboard (adityamehra799@okhdfcbank)")
    print("  4. OVERSEAS STRIPE: Send Stripe checkout links generated on Global Business Command (Port 8766)")
    print("=" * 68)
    print("DAILY CASH HUNT COMPLETED • ALL REVENUE ENGINES SYNCHRONIZED\n")

if __name__ == "__main__":
    run_daily_cash_hunt()
