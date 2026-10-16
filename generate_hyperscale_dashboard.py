#!/usr/bin/env python3
"""
generate_hyperscale_dashboard.py - Compiles Hyperscale Velocity Command Center ($1M/Mo, $1M/Wk, $1M/Day)
Generates: hyperscale_velocity_dashboard.html
"""

import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
DATA_DIR = ROOT_DIR / "data"
MODEL_PATH = DATA_DIR / "hyperscale_velocity_model.json"
OUT_HTML = ROOT_DIR / "hyperscale_velocity_dashboard.html"

def generate_dashboard():
    with open(MODEL_PATH, "r", encoding="utf-8") as f:
        model = json.load(f)

    t1 = model["tiers"]["monthly_million"]
    t2 = model["tiers"]["weekly_million"]
    t3 = model["tiers"]["daily_million"]

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aditya Mehra | Hyperscale Velocity Command Center ($1M/Mo • $1M/Wk • $1M/Day)</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #05070c;
            --bg-surface: #0a0f18;
            --bg-card: #101726;
            --border: #1a2538;
            --emerald: #10b981;
            --cyan: #06b6d4;
            --amber: #f59e0b;
            --purple: #8b5cf6;
            --rose: #f43f5e;
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
            background: linear-gradient(135deg, rgba(10, 15, 24, 0.95), rgba(16, 23, 38, 0.9));
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
            background: linear-gradient(90deg, var(--emerald), var(--cyan), var(--purple), var(--rose));
        }}
        .badge {{
            display: inline-block;
            padding: 6px 16px;
            background: rgba(16, 185, 129, 0.15);
            color: var(--emerald);
            border: 1px solid var(--emerald);
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
        }}
        .tier-deck {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
            margin-bottom: 28px;
        }}
        @media(max-width: 1100px) {{ .tier-deck {{ grid-template-columns: 1fr; }} }}
        .tier-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 28px;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .t1-border {{ border-top: 4px solid var(--cyan); }}
        .t2-border {{ border-top: 4px solid var(--purple); }}
        .t3-border {{ border-top: 4px solid var(--rose); }}
        .t-badge {{
            font-size: 12px;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.08em;
            margin-bottom: 8px;
        }}
        .t-title {{
            font-size: 32px;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 4px;
        }}
        .t-inr {{
            font-size: 14px;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 20px;
        }}
        .metric-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 13px;
        }}
        .val-num {{
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
        }}
        .portfolio-box {{
            background: rgba(255,255,255,0.02);
            border-radius: 10px;
            padding: 14px;
            margin-top: 18px;
            font-size: 12px;
            line-height: 1.5;
            color: var(--text-muted);
            border: 1px solid rgba(255,255,255,0.05);
        }}
        .val-card {{
            margin-top: 18px;
            background: rgba(16, 185, 129, 0.05);
            border: 1px dashed var(--emerald);
            border-radius: 10px;
            padding: 12px 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
    </style>
</head>
<body>

    <div class="header">
        <div>
            <h1 style="font-size: 26px; font-weight: 800;">ADITYA MEHRA | HYPERSCALE VELOCITY CAPITAL MATRIX</h1>
            <p style="color: var(--text-muted); font-size: 14px; margin-top: 4px;">Universal Cadence Projections: $1M/Month • $1M/Week • $1M/Day | Sovereign Enterprise Operations</p>
        </div>
        <div style="text-align: right;">
            <span class="badge">EBITDA MARGIN: 97.2% – 97.5%</span>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: 6px; font-family: 'JetBrains Mono';">Infrastructure: Autonomous Agent Grid • Port 5678 Active</div>
        </div>
    </div>

    <div class="tier-deck">
        <!-- TIER 1 -->
        <div class="tier-card t1-border">
            <div>
                <div class="t-badge" style="color: var(--cyan);">Cadence Alpha</div>
                <div class="t-title" style="color: var(--cyan);">$1,000,000 <span style="font-size: 18px;">/ MO</span></div>
                <div class="t-inr">INR 8.50 Crore / Month (INR 102 Cr / Year)</div>

                <div class="metric-row">
                    <span>Daily Cashflow Velocity</span>
                    <span class="val-num" style="color: var(--cyan);">${t1['metrics_usd']['daily_usd']:,.0f} / day (₹{t1['metrics_inr']['daily_inr']:,.0f})</span>
                </div>
                <div class="metric-row">
                    <span>Weekly Run-Rate</span>
                    <span class="val-num">${t1['metrics_usd']['weekly_usd']:,.0f} / week</span>
                </div>
                <div class="metric-row">
                    <span>Annual Recurring Revenue</span>
                    <span class="val-num" style="color: var(--emerald);">${t1['metrics_usd']['annual_arr_usd']:,.0f} USD ARR</span>
                </div>
                <div class="metric-row">
                    <span>Monthly Cloud & API Opex</span>
                    <span class="val-num">${t1['unit_economics']['monthly_opex_usd']:,.0f} USD</span>
                </div>
                <div class="metric-row">
                    <span>Net EBITDA Margin</span>
                    <span class="val-num" style="color: var(--amber);">{t1['unit_economics']['ebitda_margin_pct']}%</span>
                </div>

                <div class="portfolio-box">
                    <strong>Capacity Model:</strong><br>
                    {t1['unit_economics']['client_portfolio']}
                </div>
            </div>

            <div class="val-card">
                <span style="font-size: 12px; color: var(--text-muted);">Enterprise Valuation:</span>
                <strong style="color: var(--emerald); font-family: 'JetBrains Mono'; font-size: 16px;">${t1['unit_economics']['enterprise_valuation_usd'] / 1e6:,.0f}M USD (₹{t1['unit_economics']['enterprise_valuation_inr'] / 1e7:,.0f} Cr)</strong>
            </div>
        </div>

        <!-- TIER 2 -->
        <div class="tier-card t2-border">
            <div>
                <div class="t-badge" style="color: var(--purple);">Cadence Beta</div>
                <div class="t-title" style="color: var(--purple);">$1,000,000 <span style="font-size: 18px;">/ WK</span></div>
                <div class="t-inr">INR 8.50 Crore / Week (INR 442 Cr / Year)</div>

                <div class="metric-row">
                    <span>Daily Cashflow Velocity</span>
                    <span class="val-num" style="color: var(--purple);">${t2['metrics_usd']['daily_usd']:,.0f} / day (₹{t2['metrics_inr']['daily_inr']:,.0f})</span>
                </div>
                <div class="metric-row">
                    <span>Monthly Run-Rate (MRR)</span>
                    <span class="val-num">${t2['metrics_usd']['monthly_usd']:,.0f} / month</span>
                </div>
                <div class="metric-row">
                    <span>Annual Recurring Revenue</span>
                    <span class="val-num" style="color: var(--emerald);">${t2['metrics_usd']['annual_arr_usd']:,.0f} USD ARR</span>
                </div>
                <div class="metric-row">
                    <span>Monthly Cloud & API Opex</span>
                    <span class="val-num">${t2['unit_economics']['monthly_opex_usd']:,.0f} USD</span>
                </div>
                <div class="metric-row">
                    <span>Net EBITDA Margin</span>
                    <span class="val-num" style="color: var(--amber);">{t2['unit_economics']['ebitda_margin_pct']}%</span>
                </div>

                <div class="portfolio-box">
                    <strong>Capacity Model:</strong><br>
                    {t2['unit_economics']['client_portfolio']}
                </div>
            </div>

            <div class="val-card">
                <span style="font-size: 12px; color: var(--text-muted);">Enterprise Valuation:</span>
                <strong style="color: var(--purple); font-family: 'JetBrains Mono'; font-size: 16px;">${t2['unit_economics']['enterprise_valuation_usd'] / 1e6:,.0f}M USD (₹{t2['unit_economics']['enterprise_valuation_inr'] / 1e7:,.0f} Cr)</strong>
            </div>
        </div>

        <!-- TIER 3 -->
        <div class="tier-card t3-border">
            <div>
                <div class="t-badge" style="color: var(--rose);">Cadence Gamma (Planetary Unicorn)</div>
                <div class="t-title" style="color: var(--rose);">$1,000,000 <span style="font-size: 18px;">/ DAY</span></div>
                <div class="t-inr">INR 8.50 Crore / Day (INR 3,102 Cr / Year)</div>

                <div class="metric-row">
                    <span>Weekly Run-Rate</span>
                    <span class="val-num" style="color: var(--rose);">${t3['metrics_usd']['weekly_usd']:,.0f} / week</span>
                </div>
                <div class="metric-row">
                    <span>Monthly Run-Rate (MRR)</span>
                    <span class="val-num">${t3['metrics_usd']['monthly_usd']:,.0f} / month</span>
                </div>
                <div class="metric-row">
                    <span>Annual Recurring Revenue</span>
                    <span class="val-num" style="color: var(--emerald);">${t3['metrics_usd']['annual_arr_usd']:,.0f} USD ARR</span>
                </div>
                <div class="metric-row">
                    <span>Monthly Cloud & API Opex</span>
                    <span class="val-num">${t3['unit_economics']['monthly_opex_usd']:,.0f} USD</span>
                </div>
                <div class="metric-row">
                    <span>Net EBITDA Margin</span>
                    <span class="val-num" style="color: var(--amber);">{t3['unit_economics']['ebitda_margin_pct']}%</span>
                </div>

                <div class="portfolio-box">
                    <strong>Capacity Model:</strong><br>
                    {t3['unit_economics']['client_portfolio']}
                </div>
            </div>

            <div class="val-card">
                <span style="font-size: 12px; color: var(--text-muted);">Enterprise Valuation:</span>
                <strong style="color: var(--rose); font-family: 'JetBrains Mono'; font-size: 16px;">${t3['unit_economics']['enterprise_valuation_usd'] / 1e9:,.2f}B USD (₹{t3['unit_economics']['enterprise_valuation_inr'] / 1e7:,.0f} Cr Decacorn)</strong>
            </div>
        </div>
    </div>

</body>
</html>
"""
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[OK] Generated Hyperscale Velocity Dashboard: {OUT_HTML}")

if __name__ == "__main__":
    generate_dashboard()
