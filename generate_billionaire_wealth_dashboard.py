#!/usr/bin/env python3
"""
generate_billionaire_wealth_dashboard.py - Compiles Billionaires, Family Offices & Mega-Deals Command Center
Generates: billionaire_wealth_dashboard.html
"""

import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "omega_unified_master.db"
MODEL_PATH = DATA_DIR / "billionaire_wealth_intelligence_model.json"
OUT_HTML = ROOT_DIR / "billionaire_wealth_dashboard.html"

def generate_dashboard():
    with open(MODEL_PATH, "r", encoding="utf-8") as f:
        model = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT principal_name, flagship_enterprise, net_worth_scale, headquarters, family_office_entity, target_role, compensation_range, operational_pitch
        FROM billionaire_family_offices
        LIMIT 40
    """)
    billionaires = c.fetchall()

    c.execute("""
        SELECT deal_name, deal_type, deal_size_usd, deal_size_inr, target_industry, advisory_margin_pct, key_levers
        FROM million_dollar_deal_archetypes
    """)
    deals = c.fetchall()
    conn.close()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aditya Mehra | Billionaires, Family Offices & Mega-Deals Intelligence Center</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #06090e;
            --bg-surface: #0b111a;
            --bg-card: #121a29;
            --border: #1d2a3f;
            --amber: #f59e0b;
            --gold: #fbbf24;
            --emerald: #10b981;
            --cyan: #06b6d4;
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
            background: linear-gradient(135deg, rgba(11, 17, 26, 0.95), rgba(18, 26, 41, 0.9));
            border: 1px solid var(--border);
            border-radius: 20px;
            margin-bottom: 24px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 50px rgba(0,0,0,0.6);
        }}
        .header::after {{
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--gold), var(--amber), var(--emerald), var(--cyan));
        }}
        .badge {{
            display: inline-block;
            padding: 6px 16px;
            background: rgba(245, 158, 11, 0.15);
            color: var(--gold);
            border: 1px solid var(--gold);
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
        }}
        .grid-4 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }}
        .kpi-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 22px;
            position: relative;
        }}
        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 3px;
            background: var(--gold);
        }}
        .kpi-val {{
            font-size: 30px;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            color: var(--gold);
            margin: 8px 0 4px;
        }}
        .kpi-lbl {{
            font-size: 13px;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.05em;
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
            color: var(--gold);
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
        .tag-pill {{
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            display: inline-block;
        }}
        .tag-gold {{ background: rgba(251, 191, 36, 0.15); color: var(--gold); border: 1px solid var(--gold); }}
        .tag-emerald {{ background: rgba(16, 185, 129, 0.15); color: var(--emerald); border: 1px solid var(--emerald); }}
        .deal-box {{
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 14px;
        }}
    </style>
</head>
<body>

    <div class="header">
        <div>
            <h1 style="font-size: 26px; font-weight: 800;">ADITYA MEHRA | BILLIONAIRE & MEGA-DEAL INTELLIGENCE</h1>
            <p style="color: var(--text-muted); font-size: 14px; margin-top: 4px;">Sovereign Directory of 140+ Promoters, Family Offices, Global Titans & $1M–$25M Deal Archetypes</p>
        </div>
        <div style="text-align: right;">
            <span class="badge">140 BILLIONAIRES INDEXED</span>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: 6px; font-family: 'JetBrains Mono';">PremjiInvest • Catamaran • Rainmatter • Global Titans</div>
        </div>
    </div>

    <div class="grid-4">
        <div class="kpi-card">
            <div class="kpi-lbl">Total Billionaires & Family Offices</div>
            <div class="kpi-val">{model['total_billionaires_indexed']}</div>
            <div style="font-size: 12px; color: var(--text-muted);">Indexed in omega_unified_master.db</div>
        </div>
        <div class="kpi-card" style="border-top: 3px solid var(--emerald);">
            <div class="kpi-lbl">Mega-Deal Archetypes</div>
            <div class="kpi-val" style="color: var(--emerald);">{model['deal_archetypes_count']} Archetypes</div>
            <div style="font-size: 12px; color: var(--emerald);">$1.2M to $25M USD Deal Sizes</div>
        </div>
        <div class="kpi-card" style="border-top: 3px solid var(--cyan);">
            <div class="kpi-lbl">Top Executive Comp Range</div>
            <div class="kpi-val" style="color: var(--cyan);">₹14L – ₹20L+</div>
            <div style="font-size: 12px; color: var(--cyan);">Founders' Office & Investment Associates</div>
        </div>
        <div class="kpi-card" style="border-top: 3px solid var(--purple);">
            <div class="kpi-lbl">Ecosystems Covered</div>
            <div class="kpi-val" style="color: var(--purple);">5 Wealth Hubs</div>
            <div style="font-size: 12px; color: var(--purple);">Bengaluru • Mumbai • US • APAC</div>
        </div>
    </div>

    <div class="grid-2">
        <div class="panel">
            <div class="panel-title"><span>👑</span> Verified Billionaires, Family Offices & Executive Promoters</div>
            <table>
                <thead>
                    <tr>
                        <th>Principal / Promoter</th>
                        <th>Enterprise / Fund</th>
                        <th>Net Worth Scale</th>
                        <th>Family Office Entity</th>
                        <th>Target High-Comp Role</th>
                        <th>Comp Range</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(f'''<tr>
                        <td style="font-weight: 700; color: #fff;">{b[0]}</td>
                        <td style="color: var(--text-muted);">{b[1]}</td>
                        <td><span class="tag-pill tag-gold">{b[2]}</span></td>
                        <td style="font-size: 12px;">{b[4][:30]}</td>
                        <td style="font-size: 12px; color: var(--cyan);">{b[5]}</td>
                        <td style="font-family: 'JetBrains Mono'; font-weight: 700; color: var(--emerald);">{b[6]}</td>
                    </tr>''' for b in billionaires)}
                </tbody>
            </table>
        </div>

        <div>
            <div class="panel">
                <div class="panel-title"><span>💼</span> Multi-Million Dollar Deal Archetypes ($1M – $25M)</div>
                {''.join(f'''<div class="deal-box">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <strong style="color: var(--gold); font-size: 15px;">{d[0]}</strong>
                        <span class="tag-pill tag-emerald">{d[1]}</span>
                    </div>
                    <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 8px;">Target Industry: {d[4]}</div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-family: 'JetBrains Mono'; font-size: 13px;">
                        <span>Deal Size: <strong style="color: #fff;">${d[2]:,.0f} USD</strong> (INR {d[3] / 1e7:,.1f} Cr)</span>
                        <span style="color: var(--amber);">Margin: {d[5]}%</span>
                    </div>
                    <div style="font-size: 12px; color: var(--text-muted); border-top: 1px dashed var(--border); padding-top: 6px; font-style: italic;">
                        Levers: {d[6]}
                    </div>
                </div>''' for d in deals)}
            </div>
        </div>
    </div>

</body>
</html>
"""
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[OK] Generated Billionaire Wealth Dashboard: {OUT_HTML}")

if __name__ == "__main__":
    generate_dashboard()
