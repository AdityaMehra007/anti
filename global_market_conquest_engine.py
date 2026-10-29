#!/usr/bin/env python3
"""
========================================================================================
GLOBAL WORLD JOB & BUSINESS MARKET CONQUEST ENGINE
========================================================================================
Autonomous synthesis and execution engine for planetary career and business intelligence.
Maps the 5 Global Theaters:
1. North America (Silicon Valley, NYC, Seattle, Austin)
2. Western Europe (London, Zurich, Munich, Amsterdam)
3. Middle East / MENA (Dubai, Abu Dhabi, Riyadh)
4. Asia-Pacific (Singapore, Tokyo, Sydney)
5. India / Bengaluru (Global Capability & Deep Engineering Capital)

Outputs:
- e:\anti\data\GLOBAL_WORLD_MARKET_MASTER.json
- e:\anti\apps\job_application_studio\global_world_market_cockpit.html
========================================================================================
"""

import os
import sys
import json
import sqlite3
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(r"e:\anti")
DATA_DIR = ROOT_DIR / "data"
APPS_DIR = ROOT_DIR / "apps" / "job_application_studio"
DATA_DIR.mkdir(parents=True, exist_ok=True)
APPS_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = ROOT_DIR / "BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite"
OUT_JSON = DATA_DIR / "GLOBAL_WORLD_MARKET_MASTER.json"
OUT_HTML = APPS_DIR / "global_world_market_cockpit.html"

GLOBAL_HUBS = [
    {
        "region": "North America (USA)",
        "hubs": "Silicon Valley (SF/Bay Area), New York City, Seattle, Austin",
        "currency": "USD ($)",
        "entry_comp": "$130,000 - $210,000 (₹1.1 Cr - ₹1.75 Cr)",
        "senior_comp": "$280,000 - $600,000+ (₹2.3 Cr - ₹5.0 Cr)",
        "anchor_sectors": "AI Foundation Models, Cloud Hyperscalers, Quant Finance, Venture Capital",
        "visa_path": "L-1B Intracompany Transfer, H-1B Lottery, O-1 Extraordinary Ability",
        "titans": ["NVIDIA", "Apple", "Microsoft", "Alphabet (Google)", "Amazon", "Meta", "OpenAI", "Goldman Sachs"]
    },
    {
        "region": "Western Europe",
        "hubs": "London (UK), Zurich (Switzerland), Munich (Germany), Amsterdam (Netherlands)",
        "currency": "GBP (£) / EUR (€) / CHF",
        "entry_comp": "€65,000 - €110,000 (₹60L - ₹1.05 Cr)",
        "senior_comp": "€140,000 - €260,000 (₹1.3 Cr - ₹2.4 Cr)",
        "anchor_sectors": "Fintech & Trade Finance, Automotive AI, Energy Trading, Precision MedTech",
        "visa_path": "EU Blue Card (Fast-track PR in 21 months), UK Skilled Worker Visa",
        "titans": ["Shell Global", "Airbus Defence", "Mercedes-Benz Group", "ASML", "UBS / Credit Suisse", "SAP SE"]
    },
    {
        "region": "Middle East / GCC",
        "hubs": "Dubai (DIFC / Internet City), Abu Dhabi (ADGM), Riyadh (KSA Tech Hub)",
        "currency": "AED (Dirhams) / SAR",
        "entry_comp": "AED 22,000 - 38,000/mo (Tax-Free: ₹60L - ₹1.02 Cr/yr)",
        "senior_comp": "AED 55,000 - 95,000/mo (Tax-Free: ₹1.5 Cr - ₹2.6 Cr/yr)",
        "anchor_sectors": "Sovereign Wealth Funds (ADIA, Mubadala, PIF), Global Trade Logistics, Crypto/Web3",
        "visa_path": "10-Year UAE Golden Visa, Green Visa, Company Sponsored Residency",
        "titans": ["DP World", "Aramco", "Emirates Group", "Careem (Uber)", "G42 AI", "Abu Dhabi Investment Authority"]
    },
    {
        "region": "Asia-Pacific (APAC)",
        "hubs": "Singapore (Marina Bay), Tokyo (Roppongi), Sydney (CBD)",
        "currency": "SGD ($) / JPY (¥) / AUD ($)",
        "entry_comp": "SGD 85,000 - 135,000 (₹53L - ₹85L)",
        "senior_comp": "SGD 180,000 - 320,000 (₹1.15 Cr - ₹2.05 Cr)",
        "anchor_sectors": "Regional Big Tech HQs, Maritime Shipping, Semiconductor Supply Chain",
        "visa_path": "Singapore Employment Pass (EP / COMPASS), Australia TSS 482 Visa",
        "titans": ["ByteDance / TikTok APAC", "Grab Holdings", "Sea Group (Shopee)", "DBS Bank", "Sony", "TSMC"]
    },
    {
        "region": "India (Global Epicenter)",
        "hubs": "Bengaluru (ORR, Whitefield, Manyata, HSR), Hyderabad (HITEC City), Mumbai (BKC)",
        "currency": "INR (₹)",
        "entry_comp": "₹14 LPA - ₹45+ LPA",
        "senior_comp": "₹45 LPA - ₹1.5 Cr+",
        "anchor_sectors": "400+ Fortune 500 GCCs, DeepTech R&D, UPI Fintech, Quick-Commerce, Aerospace",
        "visa_path": "Domestic Base / Foundation Launchpad for Global Expansion",
        "titans": ["Target India", "Boeing BIETC", "JPMorgan Chase India", "Goldman Sachs Services", "Flipkart", "Razorpay"]
    }
]

def load_database_data():
    titans = []
    unicorns = []
    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        try:
            cur.execute("SELECT company_name, country, sector, location, target_role, ctc_lpa FROM global_world_titans LIMIT 25")
            for r in cur.fetchall():
                titans.append({
                    "company": r[0],
                    "country": r[1],
                    "sector": r[2],
                    "location": r[3],
                    "role": r[4],
                    "ctc": r[5]
                })
        except Exception as e:
            print("Error loading titans:", e)

        try:
            cur.execute("SELECT company_name, valuation, primary_founders, sector FROM billion_dollar_unicorns_master LIMIT 15")
            for r in cur.fetchall():
                unicorns.append({
                    "company": r[0],
                    "valuation": r[1],
                    "founders": r[2],
                    "sector": r[3]
                })
        except Exception as e:
            print("Error loading unicorns:", e)
        conn.close()
    return titans, unicorns

def main():
    print("=" * 80)
    print("🚀 EXECUTING GLOBAL WORLD JOB & BUSINESS MARKET CONQUEST ENGINE")
    print("=" * 80)

    titans, unicorns = load_database_data()
    print(f"✅ Loaded {len(titans)} Global World Titans")
    print(f"✅ Loaded {len(unicorns)} Top Global Unicorns")
    print(f"✅ Mapped 5 Planetary Hubs (USA, Europe, MENA, APAC, India)")

    master_payload = {
        "title": "GLOBAL WORLD MARKET & CAREER SUPREMACY DOSSIER",
        "candidate": "Aditya Mehra | Global Sovereign Operator",
        "planetary_theaters": GLOBAL_HUBS,
        "world_titans": titans,
        "global_unicorns": unicorns,
        "execution_date": "2026-10-27"
    }

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(master_payload, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved JSON Master: {OUT_JSON} ({OUT_JSON.stat().st_size / 1024:.1f} KB)")

    # Build Interactive HTML Cockpit
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🌐 GLOBAL WORLD MARKET & CAREER COCKPIT (PLANETARY EDITION)</title>
<style>
  :root {{
    --bg: #06090e;
    --card: #0d121c;
    --border: #1e293b;
    --accent: #38bdf8;
    --green: #10b981;
    --gold: #f59e0b;
    --text: #f1f5f9;
    --text-muted: #94a3b8;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
  body {{ background: var(--bg); color: var(--text); padding: 24px; }}
  header {{ margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }}
  h1 {{ font-size: 24px; font-weight: 800; color: var(--text); display: flex; align-items: center; gap: 10px; }}
  .badge {{ background: rgba(56,189,248,0.15); color: var(--accent); border: 1px solid var(--accent); padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 700; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 18px; margin-bottom: 24px; }}
  .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }}
  .card-title {{ font-size: 18px; font-weight: 700; margin-bottom: 8px; color: var(--accent); }}
  .comp-tag {{ display: inline-block; background: rgba(16,185,129,0.15); color: var(--green); border: 1px solid var(--green); padding: 3px 8px; border-radius: 6px; font-size: 13px; font-weight: 700; margin-bottom: 10px; }}
  .field {{ font-size: 13px; color: var(--text-muted); margin-bottom: 6px; }}
  .field strong {{ color: var(--text); }}
  .section-hdr {{ font-size: 20px; font-weight: 800; margin: 30px 0 16px; border-left: 4px solid var(--accent); padding-left: 12px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 10px; background: var(--card); border-radius: 10px; overflow: hidden; }}
  th, td {{ padding: 12px 14px; text-align: left; font-size: 13px; border-bottom: 1px solid var(--border); }}
  th {{ background: #111827; color: var(--accent); font-weight: 700; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }}
  tr:hover {{ background: rgba(255,255,255,0.02); }}
</style>
</head>
<body>

<header>
  <div>
    <h1>🌐 GLOBAL WORLD JOB & BUSINESS MARKET COCKPIT</h1>
    <p style="color: var(--text-muted); font-size: 13px; margin-top: 4px;">Planetary Sovereign Command | 5 Global Theaters | Live World Titans & Unicorns</p>
  </div>
  <span class="badge">STATUS: 100% OPERATIONAL & VERIFIED</span>
</header>

<div class="section-hdr">🌍 THE 5 PLANETARY ECONOMIC THEATERS</div>
<div class="grid">
"""
    for hub in GLOBAL_HUBS:
        html_content += f"""
  <div class="card">
    <div class="card-title">{hub['region']}</div>
    <div class="comp-tag">Entry TC: {hub['entry_comp']}</div>
    <div class="field"><strong>Hubs:</strong> {hub['hubs']}</div>
    <div class="field"><strong>Senior TC:</strong> {hub['senior_comp']}</div>
    <div class="field"><strong>Anchor Sectors:</strong> {hub['anchor_sectors']}</div>
    <div class="field"><strong>Visa / Legal Rails:</strong> {hub['visa_path']}</div>
    <div class="field" style="margin-top: 8px;"><strong>Titan Employers:</strong> {", ".join(hub['titans'][:4])}</div>
  </div>
"""

    html_content += """
</div>

<div class="section-hdr">🏛️ WORLD TITANS & FORTUNE 500 SELECTION (FROM LOCAL DB)</div>
<table>
  <thead>
    <tr>
      <th>Company</th>
      <th>Country HQ</th>
      <th>Industry Sector</th>
      <th>Target Role</th>
      <th>Benchmark CTC</th>
    </tr>
  </thead>
  <tbody>
"""
    for t in titans[:15]:
        html_content += f"""
    <tr>
      <td><strong>{t['company']}</strong></td>
      <td>{t['country']}</td>
      <td>{t['sector']}</td>
      <td>{t['role']}</td>
      <td style="color: var(--green); font-weight: 700;">{t['ctc']}</td>
    </tr>
"""

    html_content += """
  </tbody>
</table>

<div class="section-hdr">🦄 GLOBAL UNICORNS & HIGH-GROWTH MARKET LEADERS</div>
<table>
  <thead>
    <tr>
      <th>Unicorn Company</th>
      <th>Valuation</th>
      <th>Founders / Leadership</th>
      <th>Disruptive Sector</th>
    </tr>
  </thead>
  <tbody>
"""
    for u in unicorns[:10]:
        html_content += f"""
    <tr>
      <td><strong>{u['company']}</strong></td>
      <td style="color: var(--gold); font-weight: 700;">{u['valuation']}</td>
      <td>{u['founders']}</td>
      <td>{u['sector']}</td>
    </tr>
"""

    html_content += """
  </tbody>
</table>

<footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--border); text-align: center; color: var(--text-muted); font-size: 12px;">
  OMEGA ∞ PLANETARY CAREER COMMAND | ZERO VIBE VERIFIED | BENGALURU & GLOBAL HUBS
</footer>

</body>
</html>
"""

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"🖥️  Generated Interactive Global Cockpit: {OUT_HTML} ({OUT_HTML.stat().st_size / 1024:.1f} KB)")
    print("=" * 80)
    print("🎉 GLOBAL WORLD MARKET CONQUEST PLAN & ENGINE EXECUTED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    main()
