#!/usr/bin/env python3
"""
Summer 2027 Internship Master Processor & Application Suite
Extracts, structures, categorizes, and generates an interactive application tracker
from SimplifyJobs/Summer2027-Internships dataset.
"""

import json
import csv
import os
from datetime import datetime
from collections import Counter

TIER_1_FIRMS = {
    "Google", "Alphabet", "Meta", "Apple", "Microsoft", "Amazon", "Netflix", "NVIDIA",
    "OpenAI", "Anthropic", "Tesla", "ByteDance", "TikTok", "Uber", "Airbnb", "Stripe",
    "Databricks", "Snowflake", "Palantir", "Salesforce", "Adobe", "Oracle", "Cisco",
    "Jane Street", "Citadel", "Citadel Securities", "Hudson River Trading", "Two Sigma",
    "Jump Trading", "DRW", "Optiver", "SIG", "Susquehanna", "DE Shaw", "D. E. Shaw",
    "Point72", "Five Rings", "Radix Trading", "Valkyrie Trading", "Goldman Sachs",
    "Morgan Stanley", "JPMorgan Chase", "Bank of America", "Royal Bank of Canada",
    "AMD", "Intel", "Qualcomm", "Broadcom", "Marvell", "ASML", "Arm", "Waymo"
}

QUANT_FIRMS = {
    "Jane Street", "Citadel", "Citadel Securities", "Hudson River Trading", "Two Sigma",
    "Jump Trading", "DRW", "Optiver", "SIG", "Susquehanna", "DE Shaw", "D. E. Shaw",
    "Point72", "Five Rings", "Radix Trading", "Valkyrie Trading", "Flow Traders", "IMC Trading",
    "Akuna Capital", "TransMarket Group", "Old Mission", "Belvedere Trading", "Tower Research Capital"
}

def clean_category(cat: str) -> str:
    if not cat:
        return "Software"
    cat_lower = cat.lower()
    if "ai" in cat_lower or "ml" in cat_lower or "data" in cat_lower:
        return "AI/ML/Data"
    if "quant" in cat_lower:
        return "Quant"
    if "hardware" in cat_lower:
        return "Hardware"
    if "product" in cat_lower:
        return "Product"
    if "software" in cat_lower:
        return "Software"
    return cat

def is_remote_job(locations: list, title: str) -> bool:
    if any("remote" in str(loc).lower() for loc in locations):
        return True
    if "remote" in title.lower():
        return True
    return False

def determine_tier(company: str, category: str) -> str:
    if company in QUANT_FIRMS or category == "Quant":
        return "Quant / Prop Trading"
    if company in TIER_1_FIRMS:
        return "Tier 1 / Big Tech"
    return "Enterprise / High Growth"

def format_date(timestamp) -> str:
    if not timestamp:
        return "Recent"
    try:
        ts = int(timestamp)
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
    except Exception:
        return "Recent"

def main():
    json_path = r"e:\anti\Summer2027-Internships\.github\scripts\listings.json"
    os.makedirs(r"e:\anti\data", exist_ok=True)

    print(f"Loading listings from {json_path}...")
    with open(json_path, "r", encoding="utf-8") as f:
        listings = json.load(f)

    print(f"Total raw listings: {len(listings)}")

    # Filter active and visible
    active_listings = [l for l in listings if l.get("active") and l.get("is_visible", True)]
    print(f"Total active & visible listings: {len(active_listings)}")

    processed_all = []
    processed_2027 = []

    for l in active_listings:
        company = l.get("company_name", "Unknown").strip()
        title = l.get("title", "Intern").strip()
        cat = clean_category(l.get("category", "Software"))
        locations = l.get("locations", [])
        if isinstance(locations, str):
            locations = [locations]
        loc_str = ", ".join(locations) if locations else "United States"
        terms = l.get("terms", [])
        remote = is_remote_job(locations, title)
        tier = determine_tier(company, cat)
        date_posted = format_date(l.get("date_posted"))
        date_updated = format_date(l.get("date_updated"))
        url = l.get("url", "")
        company_url = l.get("company_url", "")
        sponsorship = l.get("sponsorship", "Other")
        degrees = l.get("degrees", [])

        # Simplify direct apply helper
        simplify_id = l.get("id", "")
        simplify_apply = f"https://simplify.jobs/p/{simplify_id}" if simplify_id else ""

        item = {
            "id": simplify_id,
            "company": company,
            "title": title,
            "category": cat,
            "locations": loc_str,
            "is_remote": remote,
            "terms": terms,
            "sponsorship": sponsorship,
            "degrees": degrees,
            "tier": tier,
            "date_posted": date_posted,
            "date_updated": date_updated,
            "apply_url": url,
            "simplify_url": simplify_apply,
            "company_url": company_url
        }

        processed_all.append(item)
        if any("2027" in t for t in terms):
            processed_2027.append(item)

    print(f"Processed active records: {len(processed_all)}")
    print(f"Processed 2027 active records: {len(processed_2027)}")

    # Save JSON files
    with open(r"e:\anti\data\summer2027_active.json", "w", encoding="utf-8") as f:
        json.dump(processed_2027, f, indent=2)

    with open(r"e:\anti\data\internships_active_all.json", "w", encoding="utf-8") as f:
        json.dump(processed_all, f, indent=2)

    # Save CSV for Summer 2027
    csv_file = r"e:\anti\data\summer2027_active.csv"
    fields = ["company", "title", "category", "tier", "locations", "is_remote", "terms", "sponsorship", "degrees", "date_posted", "apply_url", "simplify_url"]
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in processed_2027:
            row_copy = row.copy()
            row_copy["terms"] = "; ".join(row["terms"])
            row_copy["degrees"] = "; ".join(row["degrees"]) if row["degrees"] else "Any"
            writer.writerow(row_copy)

    print(f"Wrote CSV to {csv_file}")

    # Top target recommendations (Big Tech + Quant + AI + Top Software)
    top_targets = [
        item for item in processed_2027
        if item["tier"] in ["Tier 1 / Big Tech", "Quant / Prop Trading"]
        or item["category"] in ["AI/ML/Data", "Quant"]
        or item["is_remote"]
    ]

    # Sort: Tier 1 & Quant first, then newest
    def target_sort_key(x):
        score = 0
        if x["tier"] == "Quant / Prop Trading":
            score += 100
        elif x["tier"] == "Tier 1 / Big Tech":
            score += 80
        if x["category"] == "AI/ML/Data":
            score += 20
        if x["is_remote"]:
            score += 10
        return -score

    top_targets.sort(key=target_sort_key)
    with open(r"e:\anti\data\summer2027_top_targets.json", "w", encoding="utf-8") as f:
        json.dump(top_targets[:500], f, indent=2)

    print(f"Identified {len(top_targets)} top target opportunities (saved top 500 to summer2027_top_targets.json)")

    # Build stats summary
    stats = {
        "total_active_all": len(processed_all),
        "total_active_2027": len(processed_2027),
        "categories": dict(Counter(x["category"] for x in processed_2027)),
        "tiers": dict(Counter(x["tier"] for x in processed_2027)),
        "remote_count": sum(1 for x in processed_2027 if x["is_remote"]),
        "top_companies": Counter(x["company"] for x in processed_2027).most_common(20)
    }
    with open(r"e:\anti\data\summer2027_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    print("\n--- SUMMARY OF SUMMER 2027 LISTINGS ---")
    print(f"Total 2027 Active: {stats['total_active_2027']}")
    print(f"Remote Positions: {stats['remote_count']}")
    print("Categories:", stats["categories"])
    print("Tiers:", stats["tiers"])
    print("Top Companies:", stats["top_companies"][:10])

if __name__ == "__main__":
    main()
