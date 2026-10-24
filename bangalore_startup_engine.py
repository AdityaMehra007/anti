#!/usr/bin/env python3
"""
Bangalore Top 500 Startups Engine & Prompt Dispatcher
Authoritative CLI tool to query, inspect, search, and export the biggest projects
and most powerful prompts for all top 500 startups in Bangalore.
"""

import sys
import os
import json
import argparse
from typing import List, Dict, Any

# Ensure UTF-8 output encoding across Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "BANGALORE_TOP_500_STARTUPS_PROJECTS_PROMPTS_MASTER.json")

def load_database() -> List[Dict[str, Any]]:
    if not os.path.exists(DATA_PATH):
        alt_path = os.path.join("E:\\anti\\data", "BANGALORE_TOP_500_STARTUPS_PROJECTS_PROMPTS_MASTER.json")
        if os.path.exists(alt_path):
            with open(alt_path, "r", encoding="utf-8") as f:
                return json.load(f)
        raise FileNotFoundError(f"Database not found at {DATA_PATH}")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def search_startups(query: str, sector: str = None, corridor: str = None, stage: str = None) -> List[Dict[str, Any]]:
    db = load_database()
    results = []
    q = query.lower() if query else ""

    for item in db:
        if q and (q not in item["company_name"].lower() and 
                  q not in item["sector"].lower() and 
                  q not in item["corridor"].lower() and 
                  q not in item["biggest_project"]["project_name"].lower()):
            continue
        if sector and sector.lower() not in item["sector"].lower():
            continue
        if corridor and corridor.lower() not in item["corridor"].lower():
            continue
        if stage and stage.lower() not in item["stage"].lower():
            continue
        results.append(item)
    return results

def print_startup_summary(item: Dict[str, Any]):
    p = item["biggest_project"]
    print(f"\n{'='*80}")
    print(f"[{item['id']}] Rank #{item['rank']} | {item['company_name'].upper()} ({item['stage']} - {item['valuation_or_funding']})")
    print(f"Sector:   {item['sector']} | Corridor: {item['corridor']}")
    print(f"Business: {item['core_business']}")
    print(f"{'-'*80}")
    print(f"BIGGEST PROJECT: {p['project_name']}")
    print(f"Pillar:          {p['architecture_pillar']}")
    print(f"Tech Stack:      {p['tech_stack']}")
    print(f"Scale KPIs:      {p['impact_metrics']}")
    print(f"Prompt Size:     {len(item['biggest_prompt']):,} characters")
    print(f"{'='*80}")

def print_full_prompt(item: Dict[str, Any]):
    print_startup_summary(item)
    print("\n--- THE BIGGEST AND MOST POWERFUL PROMPT ---")
    print(item["biggest_prompt"])
    print(f"\n{'='*80}")

def export_prompts(results: List[Dict[str, Any]], out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    count = 0
    for item in results:
        safe_name = "".join([c if c.isalnum() or c in ("-", "_") else "_" for c in item["company_name"]])
        filename = f"{item['rank']:03d}_{safe_name}.md"
        filepath = os.path.join(out_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {item['company_name']} - The Biggest & Most Powerful Project & Prompt\n\n")
            f.write(f"- **Rank**: #{item['rank']}\n")
            f.write(f"- **Sector**: {item['sector']}\n")
            f.write(f"- **Corridor**: {item['corridor']}\n")
            f.write(f"- **Stage**: {item['stage']} ({item['valuation_or_funding']})\n")
            f.write(f"- **Flagship Project**: {item['biggest_project']['project_name']}\n")
            f.write(f"- **Pillar**: {item['biggest_project']['architecture_pillar']}\n")
            f.write(f"- **Tech Stack**: {item['biggest_project']['tech_stack']}\n")
            f.write(f"- **Target KPIs**: {item['biggest_project']['impact_metrics']}\n\n")
            f.write("## The Master Execution Prompt\n\n```markdown\n")
            f.write(item["biggest_prompt"])
            f.write("\n```\n")
        count += 1
    print(f"Successfully exported {count} startup prompt specifications to: {out_dir}")

def main():
    parser = argparse.ArgumentParser(description="Bangalore Top 500 Startups Engine & Prompt Runner")
    parser.add_argument("--query", "-q", type=str, help="Search by startup name, project, or keyword")
    parser.add_argument("--sector", "-s", type=str, help="Filter by sector (e.g., FinTech, EV, SaaS)")
    parser.add_argument("--corridor", "-c", type=str, help="Filter by corridor (e.g., Koramangala, HSR, Indiranagar)")
    parser.add_argument("--stage", type=str, help="Filter by stage (e.g., Decacorn, Unicorn, Soonicorn)")
    parser.add_argument("--show-prompt", "-p", action="store_true", help="Display full prompt for matching startups")
    parser.add_argument("--top", "-t", type=int, default=10, help="Number of results to display (default: 10)")
    parser.add_argument("--export", "-e", type=str, help="Directory to export markdown prompts for matching startups")
    parser.add_argument("--stats", action="store_true", help="Display macro ecosystem statistics")

    args = parser.parse_args()

    if args.stats:
        db = load_database()
        print(f"\n=== BANGALORE TOP 500 TECH STARTUPS ECOSYSTEM TELEMETRY ===")
        print(f"Total Companies Indexed:    {len(db)}")
        total_chars = sum(len(x['biggest_prompt']) for x in db)
        print(f"Total Prompt Corpus Size:   {total_chars:,} characters (~{total_chars//4:,} tokens)")
        
        sectors = {}
        stages = {}
        for x in db:
            sectors[x["sector"]] = sectors.get(x["sector"], 0) + 1
            stages[x["stage"]] = stages.get(x["stage"], 0) + 1
        
        print("\n--- Breakdown by Sector ---")
        for s, c in sorted(sectors.items(), key=lambda x: -x[1]):
            print(f"  {s:<58}: {c:>3} companies")
            
        print("\n--- Breakdown by Stage ---")
        for st, c in sorted(stages.items(), key=lambda x: -x[1]):
            print(f"  {st:<30}: {c:>3} companies")
        print("="*60)
        return

    results = search_startups(query=args.query, sector=args.sector, corridor=args.corridor, stage=args.stage)

    if not results:
        print("No startups matched your search criteria.")
        return

    print(f"\nFound {len(results)} matching startups (showing top {min(args.top, len(results))}):")

    for item in results[:args.top]:
        if args.show_prompt:
            print_full_prompt(item)
        else:
            print_startup_summary(item)

    if args.export:
        export_prompts(results, args.export)

if __name__ == "__main__":
    main()
