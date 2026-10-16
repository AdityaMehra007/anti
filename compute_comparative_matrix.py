#!/usr/bin/env python3
import csv
import re
import json
import sys
from omniverse_analytics import calculate_bengaluru_inhand_salary, evaluate_career_leverage

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("BANGALORE_ZERO_EXP_FRESHERS_LIVE.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    jobs = list(reader)

results = []
for j in jobs:
    ctc_str = j["CTC Bracket"]
    nums = [float(x) for x in re.findall(r"(\d+\.?\d*)", ctc_str)]
    if len(nums) >= 2:
        min_ctc, max_ctc = nums[0], nums[1]
    elif len(nums) == 1:
        min_ctc = max_ctc = nums[0]
    else:
        min_ctc, max_ctc = 6.0, 8.0
    mid_ctc = round((min_ctc + max_ctc) / 2.0, 2)
    sal = calculate_bengaluru_inhand_salary(mid_ctc)

    cluster = j["Cluster / Tech Park"].lower()
    if "outer ring road" in cluster or "bellandur" in cluster:
        friction = 45
        zone = "ORR (Tech Corridor)"
    elif "whitefield" in cluster:
        friction = 55
        zone = "East (Whitefield)"
    elif "electronic city" in cluster:
        friction = 50
        zone = "South (Electronic City)"
    elif "manyata" in cluster or "aerospace" in cluster:
        friction = 40
        zone = "North (Manyata / Airport Road)"
    elif "koramangala" in cluster or "hsr" in cluster:
        friction = 30
        zone = "South-Central (HSR / Koramangala)"
    elif "bagmane" in cluster:
        friction = 35
        zone = "Central-East (CV Raman Nagar / Domlur)"
    else:
        friction = 40
        zone = "Bengaluru Central Corridor"

    tier = j["Category"]
    leverage = evaluate_career_leverage(j["Role & Track"], tier, mid_ctc, friction)

    fit_match = re.search(r"(\d+)%", j.get("JD Fit Analysis", "95%"))
    fit_score = int(fit_match.group(1)) if fit_match else 95

    # Shift type inference
    role_lower = (j["Role & Track"] + " " + j.get("JD Fit Analysis", "")).lower()
    if "us shift" in role_lower or "night" in role_lower or "us deposits" in role_lower:
        shift = "US Shift (6:30 PM - 3:30 AM)"
    elif "apac" in role_lower or "early" in role_lower or "reinsurance" in role_lower:
        shift = "APAC Shift (6:00 AM - 3:00 PM)"
    else:
        shift = "General Day Shift (9:00 AM - 6:00 PM)"

    results.append({
        "company": j["Company"],
        "role": j["Role & Track"],
        "job_id": j.get("Job Requisition ID", "N/A"),
        "category": j["Category"],
        "cluster": j["Cluster / Tech Park"],
        "zone": zone,
        "ctc_bracket": ctc_str,
        "min_ctc": min_ctc,
        "max_ctc": max_ctc,
        "mid_ctc": mid_ctc,
        "monthly_inhand": sal["monthly_inhand"],
        "annual_inhand": sal["annual_inhand"],
        "career_leverage": leverage,
        "fit_score": fit_score,
        "shift": shift,
        "referral": j["Internal Referral Contact"],
        "portal_url": j["Portal URL"],
        "jd_fit_summary": j.get("JD Fit Analysis", "")
    })

# Write JSON for full programmatic analysis
with open("comparative_matrix_data.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"Computed matrix across {len(results)} companies.")
results.sort(key=lambda x: (x["career_leverage"], x["mid_ctc"]), reverse=True)

print("\n--- TOP 10 HIGHEST CAREER LEVERAGE ROLES ---")
for r in results[:10]:
    print(f"{r['company']} ({r['category']}) | Role: {r['role']}")
    print(f"  CTC: {r['ctc_bracket']} (Mid: {r['mid_ctc']}L) | In-Hand: INR {r['monthly_inhand']:,.0f}/mo")
    print(f"  Leverage: {r['career_leverage']}/100 | Fit: {r['fit_score']}% | Zone: {r['zone']}")
    print(f"  Shift: {r['shift']} | Referral: {r['referral']}")
    print()
