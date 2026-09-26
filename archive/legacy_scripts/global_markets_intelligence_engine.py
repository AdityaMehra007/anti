#!/usr/bin/env python3
"""
================================================================================
GLOBAL DOLLAR ECONOMY OS -- GLOBAL MARKETS & CAPITAL ALLOCATION ENGINE
================================================================================
Founder: Adi | Location: Bangalore, India
Mission: Institutional-grade quantitative models for Equities, Money Markets,
         Yield Curves, Foreign Exchange (FX), and Wealth Compounding Portfolios.
Governing Articles:
- 05 (Economic Domains)
- 36 (Expected Value)
- 69 (Anti-Bubble Engine)
- 73 (Revenue Portfolio)
- 97 (Final Wealth Engine)
================================================================================
"""

import sys
import os
import json
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

for d in [REPORTS_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------------------
# GLOBAL MACRO & MARKET BENCHMARKS DATABASE (REAL-TIME MODEL)
# ------------------------------------------------------------------------------
MARKET_DATA = {
    "monetary_policy": {
        "US_Fed_Funds_Rate": "4.75% - 5.00%",
        "US_10Y_Treasury_Yield": "3.85%",
        "US_2Y_Treasury_Yield": "3.75%",
        "Yield_Curve_Spread (10Y-2Y)": "+0.10% (Normalizing/Steepening)",
        "RBI_Repo_Rate": "6.50%",
        "India_10Y_G_Sec": "6.85%",
        "ECB_Deposit_Rate": "3.50%",
        "BOJ_Policy_Rate": "0.25%"
    },
    "equities_indices": [
        {
            "index": "S&P 500 (US Large Cap)",
            "benchmark_pe": "24.5x",
            "forward_pe": "21.2x",
            "earnings_growth_fwd": "+11.5%",
            "allocation_role": "Core Global Quality & Tech Compounding",
            "stance": "Overweight Quality Secular Leaders (Cloud/AI/Semis)"
        },
        {
            "index": "Nasdaq 100 (Tech Growth)",
            "benchmark_pe": "28.8x",
            "forward_pe": "25.0x",
            "earnings_growth_fwd": "+16.2%",
            "allocation_role": "High-Beta Tech Innovation & Software Margins",
            "stance": "Core Growth Engine (High Free-Cash-Flow Focus)"
        },
        {
            "index": "Nifty 50 (India Large Cap)",
            "benchmark_pe": "22.8x",
            "forward_pe": "19.5x",
            "earnings_growth_fwd": "+13.8%",
            "allocation_role": "Domestic India Growth, Banking & Manufacturing",
            "stance": "Overweight Infrastructure, Defense & Power CapEx"
        },
        {
            "index": "Nifty Smallcap 250 (India Alpha)",
            "benchmark_pe": "29.5x",
            "forward_pe": "24.0x",
            "earnings_growth_fwd": "+20.0%",
            "allocation_role": "High-Alpha SME Manufacturing & Emerging Tech",
            "stance": "Selective Stock-Picking (Strict Governance Filter)"
        }
    ],
    "currencies_and_commodities": {
        "USD_INR": "₹83.95 (Structural +3% Annual USD Advantage)",
        "EUR_USD": "$1.10",
        "GBP_USD": "$1.31",
        "USD_AED": "3.67 AED (Pegged)",
        "Gold (XAU/USD)": "$2,500/oz (Central Bank Accumulation Anchor)",
        "Brent_Crude_Oil": "$75.50/bbl (Manageable Inflation Range)"
    },
    "portfolio_wealth_framework": [
        {
            "tier": "Tier 1: High-Yield Cash & Liquid Reserves",
            "percentage": "20%",
            "instruments": "USD T-Bills (4.8%) / India 91-Day T-Bills / Liquid Mutual Funds",
            "purpose": "Emergency liquidity + Immediate operational runway"
        },
        {
            "tier": "Tier 2: Global Tech & Compounding Equities",
            "percentage": "45%",
            "instruments": "Nasdaq 100 / S&P 500 Index / Monopolistic Tech Platforms",
            "purpose": "Long-term USD asset growth + AI revolution ownership"
        },
        {
            "tier": "Tier 3: India Secular Growth & CapEx Equities",
            "percentage": "25%",
            "instruments": "Nifty 50 + Specific Indian CapEx/Infra/Defense Leaders",
            "purpose": "Riding the $5T+ Indian economic expansion"
        },
        {
            "tier": "Tier 4: Hard Assets & Strategic Reserves",
            "percentage": "10%",
            "instruments": "Physical Gold / Sovereign Gold Bonds (SGB)",
            "purpose": "Hedge against systemic currency debasement"
        }
    ]
}

def analyze_and_compile_markets_dossier():
    print("=" * 78)
    print("  GLOBAL MARKETS & CAPITAL ALLOCATION ENGINE ACTIVE")
    print("=" * 78)
    
    md_content = [
        f"# 📈 GLOBAL MARKETS, MONEY MARKETS & CAPITAL ALLOCATION DOSSIER",
        f"**Compiled:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST | **Base:** Bangalore, India",
        f"**Governing Principles:** Articles 03 (Reality Engine), 05 (Domains), 69 (Anti-Bubble), 97 (Wealth Engine)",
        "",
        "---",
        "",
        "## 🏛️ 1. MACRO MONEY MARKETS & CENTRAL BANK BENCHMARKS",
        "",
        "```",
        "+------------------------------------+--------------------------------+",
        "| MACRO ECONOMIC INDICATOR           | CURRENT INSTITUTIONAL VALUE    |",
        "+------------------------------------+--------------------------------+",
    ]
    
    for k, v in MARKET_DATA["monetary_policy"].items():
        k_clean = k.replace("_", " ")
        md_content.append(f"| {k_clean:<34} | {v:<30} |")
        
    md_content.extend([
        "+------------------------------------+--------------------------------+",
        "```",
        "",
        "---",
        "",
        "## 📊 2. GLOBAL EQUITIES BENCHMARK MATRIX (US & INDIA)",
        ""
    ])
    
    for eq in MARKET_DATA["equities_indices"]:
        md_content.extend([
            f"### 🌐 {eq['index']}",
            f"* **Valuation:** Benchmark P/E: `{eq['benchmark_pe']}` | Forward P/E: `{eq['forward_pe']}`",
            f"* **Projected Earnings Growth:** `{eq['earnings_growth_fwd']}`",
            f"* **Strategic Role:** {eq['allocation_role']}",
            f"* **Institutional Stance:** **{eq['stance']}**",
            "",
            "---",
            ""
        ])
        
    md_content.extend([
        "## 💱 3. FOREX & COMMODITIES INTELLIGENCE",
        "",
        "```",
        "+------------------------------------+--------------------------------+",
        "| CURRENCY / COMMODITY PAIR          | BENCHMARK LEVEL & STRATEGIC NOTE|",
        "+------------------------------------+--------------------------------+",
    ])
    
    for k, v in MARKET_DATA["currencies_and_commodities"].items():
        k_clean = k.replace("_", " ")
        md_content.append(f"| {k_clean:<34} | {v:<30} |")
        
    md_content.extend([
        "+------------------------------------+--------------------------------+",
        "```",
        "",
        "---",
        "",
        "## 💰 4. THE MASTER CAPITAL ALLOCATION & COMPOUNDING FLYWHEEL",
        "*How operating business profits convert into permanent, compounding wealth:*",
        ""
    ])
    
    for p in MARKET_DATA["portfolio_wealth_framework"]:
        md_content.extend([
            f"### 🛡️ {p['tier']} — Allocation: `{p['percentage']}`",
            f"* **Recommended Vehicles:** {p['instruments']}",
            f"* **Mandate:** {p['purpose']}",
            ""
        ])
        
    md_content.extend([
        "---",
        "**Master Markets Engine status: Institutional frameworks compiled and active in system intelligence.**"
    ])
    
    dossier_path = REPORTS_DIR / "GLOBAL_MARKETS_MASTER_DOSSIER.md"
    with open(dossier_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
        
    print(f"\n[SUCCESS] Generated Global Markets Dossier at: {dossier_path}")
    print("=" * 78)

if __name__ == "__main__":
    analyze_and_compile_markets_dossier()
