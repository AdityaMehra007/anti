#!/usr/bin/env python3
"""
generate_million_dollar_dashboard.py - Compiles High-Impact $1M ARR ($1,000,000 / ₹8.5 Cr) Command Center
Generates: million_dollar_company_dashboard.html
"""

import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "omega_unified_master.db"
MODEL_PATH = DATA_DIR / "million_dollar_company_model.json"
OUT_HTML = ROOT_DIR / "million_dollar_company_dashboard.html"

def generate_dashboard():
    with open(MODEL_PATH, "r", encoding="utf-8") as f:
        model = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, company_name, tier, target_service, annual_contract_value_usd, monthly_mrr_usd, win_probability, expected_value_usd, deal_stage 
        FROM million_dollar_pipeline 
        ORDER BY annual_contract_value_usd DESC 
        LIMIT 25
    """)
    deals = c.fetchall()
    
    c.execute("SELECT count(1), sum(annual_contract_value_usd), sum(expected_value_usd) FROM million_dollar_pipeline")
    p_cnt, p_total_acv, p_total_ev = c.fetchone()
    conn.close()

    curr = model["currency_targets"]
    econ = model["unit_economics"]
    val = model["enterprise_valuation"]

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aditya Mehra | $1,000,000 ARR Sovereign Enterprise Command Center</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #06090e;
            --bg-surface: #0b111b;
            --bg-card: #131c2d;
            --border: #1e2c45;
            --emerald: #10b981;
            --emerald-glow: rgba(16, 185, 129, 0.2);
            --cyan: #06b6d4;
            --amber: #f59e0b;
            --purple: #8b5cf6;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: var(--bg-base);
            color: var(--text-main);
            font-family: 'Plus Jakarta Sans', sans-serif;
            padding: 24px;
            min-height: 100vh;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 28px 36px;
            background: linear-gradient(135deg, rgba(11, 17, 27, 0.95), rgba(19, 28, 45, 0.9));
            border: 1px solid var(--border);
            border-radius: 20px;
            margin-bottom: 24px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            position: relative;
            overflow: hidden;
        }}
        .header::after {{
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--emerald), var(--cyan), var(--purple));
        }}
        .badge {{
            display: inline-block;
            padding: 6px 16px;
            background: var(--emerald-glow);
            color: var(--emerald);
            border: 1px solid var(--emerald);
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.05em;
        }}
        .grid-4 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }}
        .metric-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 22px;
            position: relative;
        }}
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 3px;
            background: var(--cyan);
        }}
        .val {{
            font-size: 32px;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            margin: 8px 0 4px;
        }}
        .lbl {{
            font-size: 13px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 600;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1.3fr 0.7fr;
            gap: 20px;
            margin-bottom: 24px;
        }}
        @media(max-width: 1024px) {{ .grid-2 {{ grid-template-columns: 1fr; }} }}
        .panel {{
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 26px;
        }}
        .panel-title {{
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 12px;
            color: var(--cyan);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        th, td {{
            padding: 12px 14px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        th {{
            color: var(--text-muted);
            font-weight: 700;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        tr:hover td {{
            background: rgba(255,255,255,0.02);
        }}
        .tier-pill {{
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            display: inline-block;
        }}
        .t-ent {{ background: rgba(139, 92, 246, 0.2); color: var(--purple); border: 1px solid var(--purple); }}
        .t-mid {{ background: rgba(6, 182, 212, 0.2); color: var(--cyan); border: 1px solid var(--cyan); }}
        .t-gro {{ background: rgba(16, 185, 129, 0.2); color: var(--emerald); border: 1px solid var(--emerald); }}
        .model-row {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 14px;
        }}
    </style>
</head>
<body>

    <div class="header">
        <div>
            <h1 style="font-size: 26px; font-weight: 800; letter-spacing: -0.02em;">ADITYA MEHRA | $1,000,000 ARR SOVEREIGN ENTERPRISE</h1>
            <p style="color: var(--text-muted); font-size: 14px; margin-top: 4px;">Autonomous Agency Swarm, Cross-Border EXIM Optimization & Enterprise AI Automation | Bengaluru Global Hub</p>
        </div>
        <div style="text-align: right;">
            <span class="badge">STATUS: $1M ARR FULL CAPACITY MODEL</span>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: 6px; font-family: 'JetBrains Mono';">EBITDA: {econ['ebitda_margin_pct']}% • Valuation: ${val['valuation_usd']:,.0f} USD</div>
        </div>
    </div>

    <div class="grid-4">
        <div class="metric-card" style="border-top: 3px solid var(--emerald);">
            <div class="lbl">Annual Recurring Revenue (ARR)</div>
            <div class="val" style="color: var(--emerald);">${curr['arr_usd']:,.0f} USD</div>
            <div style="font-size: 13px; color: var(--emerald); font-weight: 600;">INR {curr['arr_inr'] / 1e7:,.2f} Crore / Year</div>
        </div>
        <div class="metric-card" style="border-top: 3px solid var(--cyan);">
            <div class="lbl">Monthly Recurring Revenue (MRR)</div>
            <div class="val" style="color: var(--cyan);">${curr['mrr_usd']:,.0f} USD</div>
            <div style="font-size: 13px; color: var(--cyan); font-weight: 600;">INR {curr['mrr_inr']:,.0f} / Month</div>
        </div>
        <div class="metric-card" style="border-top: 3px solid var(--purple);">
            <div class="lbl">Enterprise Valuation (7.5x ARR)</div>
            <div class="val" style="color: var(--purple);">${val['valuation_usd']:,.0f} USD</div>
            <div style="font-size: 13px; color: var(--purple); font-weight: 600;">INR {val['valuation_inr'] / 1e7:,.2f} Crore Institutional Worth</div>
        </div>
        <div class="metric-card" style="border-top: 3px solid var(--amber);">
            <div class="lbl">Net Annual Profit (EBITDA)</div>
            <div class="val" style="color: var(--amber);">${econ['annual_net_profit_usd']:,.0f} USD</div>
            <div style="font-size: 13px; color: var(--amber); font-weight: 600;">97.5% Ultra-High Margin Model</div>
        </div>
    </div>

    <div class="grid-2">
        <div class="panel">
            <div class="panel-title"><span>🏛️</span> Scaled Enterprise Deal Pipeline (Targeting $1M ARR)</div>
            <table>
                <thead>
                    <tr>
                        <th>Company Account</th>
                        <th>Tier</th>
                        <th>Target Practice</th>
                        <th>Annual Value</th>
                        <th>Win Prob</th>
                        <th>Expected ARR</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(f'''<tr>
                        <td style="font-weight: 700;">{d[1]}</td>
                        <td><span class="tier-pill {'t-ent' if 'ENTERPRISE' in d[2] else 't-mid' if 'MIDMARKET' in d[2] else 't-gro'}">{d[2].replace('TIER_', '')}</span></td>
                        <td style="font-size: 12px; color: var(--text-muted);">{d[3][:35]}...</td>
                        <td style="font-family: 'JetBrains Mono'; font-weight: 600; color: var(--emerald);">${d[4]:,.0f}</td>
                        <td style="font-family: 'JetBrains Mono'; font-weight: 600; color: var(--cyan);">{int(d[6] * 100)}%</td>
                        <td style="font-family: 'JetBrains Mono'; font-weight: 700; color: var(--amber);">${d[7]:,.0f}</td>
                    </tr>''' for d in deals)}
                </tbody>
            </table>
        </div>

        <div>
            <div class="panel" style="margin-bottom: 20px;">
                <div class="panel-title"><span>📊</span> Unit Economics & Expense Breakdown</div>
                <div class="model-row">
                    <span style="color: var(--text-muted);">Gross Monthly Cashflow</span>
                    <strong style="color: var(--emerald); font-family: 'JetBrains Mono';">${curr['mrr_usd']:,.0f} USD</strong>
                </div>
                <div class="model-row">
                    <span style="color: var(--text-muted);">Compute & Server Infrastructure</span>
                    <span style="font-family: 'JetBrains Mono';">$350.00 USD</span>
                </div>
                <div class="model-row">
                    <span style="color: var(--text-muted);">LLM Tokens & Autonomous Inference</span>
                    <span style="font-family: 'JetBrains Mono';">$950.00 USD</span>
                </div>
                <div class="model-row">
                    <span style="color: var(--text-muted);">Corporate Legal & Regulatory Filing</span>
                    <span style="font-family: 'JetBrains Mono';">$800.00 USD</span>
                </div>
                <div class="model-row" style="border-top: 1px solid var(--border); padding-top: 14px;">
                    <strong>Net Monthly EBITDA Profit</strong>
                    <strong style="color: var(--amber); font-family: 'JetBrains Mono'; font-size: 16px;">${econ['monthly_net_profit_usd']:,.0f} USD</strong>
                </div>
                <div style="font-size: 12px; color: var(--text-muted); margin-top: 8px;">
                    Zero payroll overhead. 5-agent autonomous swarm executes sales, delivery, and invoicing.
                </div>
            </div>

            <div class="panel">
                <div class="panel-title"><span>🎯</span> Account Portfolio Distribution</div>
                <div class="model-row">
                    <div>
                        <strong>10 Enterprise Trade Clients</strong>
                        <div style="font-size: 12px; color: var(--text-muted);">Incoterms 2020 Landed Cost Audits</div>
                    </div>
                    <span style="font-family: 'JetBrains Mono'; color: var(--purple); font-weight: 700;">$35,000 / mo</span>
                </div>
                <div class="model-row">
                    <div>
                        <strong>20 Midmarket Automation Clients</strong>
                        <div style="font-size: 12px; color: var(--text-muted);">Self-Healing n8n Production DAGs</div>
                    </div>
                    <span style="font-family: 'JetBrains Mono'; color: var(--cyan); font-weight: 700;">$36,000 / mo</span>
                </div>
                <div class="model-row">
                    <div>
                        <strong>13 Growth Intelligence Licenses</strong>
                        <div style="font-size: 12px; color: var(--text-muted);">Talent Sourcing & Market Feeds</div>
                    </div>
                    <span style="font-family: 'JetBrains Mono'; color: var(--emerald); font-weight: 700;">$13,000 / mo</span>
                </div>
                <div class="model-row" style="border-top: 1px solid var(--border); padding-top: 14px;">
                    <strong>Total Monthly Target (43 Accounts)</strong>
                    <strong style="color: var(--emerald); font-family: 'JetBrains Mono'; font-size: 16px;">$84,000 / mo</strong>
                </div>
            </div>
        </div>
    </div>

</body>
</html>
"""
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[OK] Generated $1M ARR Command Center Dashboard: {OUT_HTML}")

if __name__ == "__main__":
    generate_dashboard()
