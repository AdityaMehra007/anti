#!/usr/bin/env python3
"""
========================================================================================
ANTIGRAVITY OMEGA — COMMUTE & EXPECTED VALUE (EV) SALARY ENGINE
========================================================================================
Calculates transit duration, Metro accessibility (Purple, Green, Yellow lines),
commute friction, and multi-factor Expected Value (EV) for all 4,500 Bangalore employers.
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(r"e:\anti")
DATA_DIR = ROOT_DIR / "data"
MEGA_JSON = DATA_DIR / "BANGALORE_MEGA_4500_TARGETS.json"
OUT_JSON = DATA_DIR / "BANGALORE_COMMUTE_EV_MATRIX.json"

# Candidate Base Location: Dayananda Sagar University (DSU) / South Bengaluru
CORRIDOR_COMMUTE = {
    "electronic city": {
        "travel_mins": 25,
        "metro_line": "Yellow Line (Direct from South BLR)",
        "transit_mode": "Metro / Namma Yatri EV",
        "friction_score": 15,  # Low friction
        "commute_grade": "A+"
    },
    "koramangala": {
        "travel_mins": 22,
        "metro_line": "Green Line Feeder / Direct Auto",
        "transit_mode": "EV Shuttle / Auto",
        "friction_score": 20,
        "commute_grade": "A"
    },
    "hsr layout": {
        "travel_mins": 24,
        "metro_line": "Silk Board Interchange (Yellow/Blue)",
        "transit_mode": "EV Shuttle / Auto",
        "friction_score": 22,
        "commute_grade": "A"
    },
    "central cbd": {
        "travel_mins": 35,
        "metro_line": "Green & Purple Line (Majestic / MG Road)",
        "transit_mode": "Metro Direct",
        "friction_score": 30,
        "commute_grade": "B+"
    },
    "outer ring road": {
        "travel_mins": 45,
        "metro_line": "ORR Blue Line (Silk Board to Kadubeesanahalli)",
        "transit_mode": "Volvo Vajra Bus / Company Cab",
        "friction_score": 45,
        "commute_grade": "B"
    },
    "bannerghatta road": {
        "travel_mins": 20,
        "metro_line": "Pink Line (Kalena Agrahara / Dairy Circle)",
        "transit_mode": "Auto / BMTC Bus",
        "friction_score": 18,
        "commute_grade": "A+"
    },
    "peenya industrial area": {
        "travel_mins": 55,
        "metro_line": "Green Line Direct (Yelachenahalli to Peenya)",
        "transit_mode": "Green Line Metro",
        "friction_score": 40,
        "commute_grade": "B-"
    },
    "manyata tech park": {
        "travel_mins": 65,
        "metro_line": "Blue Line / Hebbal Express Feeder",
        "transit_mode": "Enterprise Bus / Cab",
        "friction_score": 60,
        "commute_grade": "C+"
    },
    "whitefield": {
        "travel_mins": 70,
        "metro_line": "Purple Line (Baiyappanahalli to Kadugodi)",
        "transit_mode": "Purple Line Metro Train",
        "friction_score": 65,
        "commute_grade": "C"
    }
}

DEFAULT_COMMUTE = {
    "travel_mins": 40,
    "metro_line": "BMTC Metro Feeder",
    "transit_mode": "Bus / Auto",
    "friction_score": 35,
    "commute_grade": "B"
}

SECTOR_CTC_MULTIPLIERS = {
    "Investment Banking & Financial Operations": (900000, 1400000),
    "Global Capability Centers (GCCs) & Tech Giants": (850000, 1350000),
    "Enterprise SaaS, AI & Cloud Platforms": (800000, 1300000),
    "Management Consulting & Advisory Services": (750000, 1200000),
    "FinTech, Payments & Digital Banking": (750000, 1200000),
    "Aerospace, Defense & Heavy Engineering": (700000, 1150000),
    "EXIM, Ocean Freight & Global Logistics": (650000, 1100000),
    "E-Commerce, Quick-Commerce & Retail Supply Chain": (650000, 1050000),
    "Automotive, EV & Industrial Automation": (600000, 1000000),
    "Events, Experiential Media & Brand Marketing": (600000, 950000)
}

def calculate_ev(median_ctc: float, friction: int, fit_score: int) -> float:
    """Calculates normalized Expected Value index (0 - 100)."""
    # High CTC + High Fit - Low Commute Friction
    ctc_component = (median_ctc / 1400000.0) * 40.0  # Up to 40 pts
    fit_component = (fit_score / 100.0) * 40.0        # Up to 40 pts
    commute_component = max(0.0, (100 - friction) / 100.0) * 20.0 # Up to 20 pts
    return round(ctc_component + fit_component + commute_component, 1)

def main():
    print("=" * 75)
    print("      ANTIGRAVITY OMEGA — COMMUTE & EV SALARY MATRIX ENGINE")
    print("=" * 75)

    if not MEGA_JSON.exists():
        print(f"Error: {MEGA_JSON} not found!")
        return

    with open(MEGA_JSON, "r", encoding="utf-8") as f:
        targets = json.load(f)

    print(f"Analyzing commute and EV for {len(targets)} Bangalore employers...")

    enriched = []
    for t in targets:
        corr_lower = t["corridor"].lower()
        matched_commute = DEFAULT_COMMUTE
        for k, v in CORRIDOR_COMMUTE.items():
            if k in corr_lower:
                matched_commute = v
                break

        # CTC Band calculation
        sec = t.get("sector", "")
        min_ctc, max_ctc = SECTOR_CTC_MULTIPLIERS.get(sec, (600000, 1000000))
        median_ctc = (min_ctc + max_ctc) / 2.0

        ev_score = calculate_ev(median_ctc, matched_commute["friction_score"], t.get("fit_score", 90))

        item = {
            "id": t["id"],
            "company": t["company"],
            "sector": t["sector"],
            "corridor": t["corridor"],
            "hr_email": t["hr_email"],
            "travel_mins": matched_commute["travel_mins"],
            "transit_mode": matched_commute["transit_mode"],
            "metro_line": matched_commute["metro_line"],
            "commute_grade": matched_commute["commute_grade"],
            "ctc_min_inr": min_ctc,
            "ctc_max_inr": max_ctc,
            "ctc_median_inr": median_ctc,
            "ev_career_score": ev_score
        }
        enriched.append(item)

    # Sort by EV Career Score descending
    enriched.sort(key=lambda x: x["ev_career_score"], reverse=True)

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2)

    print(f"Saved Commute & EV Matrix: {OUT_JSON}")
    print(f"Top EV Employer: {enriched[0]['company']} (EV: {enriched[0]['ev_career_score']}, {enriched[0]['commute_grade']} Commute: {enriched[0]['travel_mins']} mins)")
    print("=" * 75)

if __name__ == "__main__":
    main()
