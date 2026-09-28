#!/usr/bin/env python3
"""
CLI Query Utility for Remote Work Ecosystem with Multi-Metric Scoring
Usage:
  python query_remote_jobs.py --search "AI"
  python query_remote_jobs.py --tier1
  python query_remote_jobs.py --tag "4-Day Week"
  python query_remote_jobs.py --companies
  python query_remote_jobs.py --stats
"""

import sys
import os
import json
import argparse

def load_ecosystem():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'remote_ecosystem_master.json')
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        sys.exit(1)
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def print_item(item, idx=None):
    prefix = f"[{idx}] " if idx is not None else "• "
    tags_str = f" [{', '.join(item.get('tags', []))}]" if item.get('tags') else ""
    
    scoring = item.get('scoring', {})
    score_str = f" [*] {scoring.get('composite_score', 'N/A')}/100" if scoring else ""
    tier_str = f" ({scoring.get('strategic_tier', '')})" if scoring.get('strategic_tier') else ""

    print(f"\n{prefix}\033[1;36m{item['title']}\033[0m \033[1;33m{score_str}\033[0m\033[1;35m{tier_str}\033[0m{tags_str}")
    print(f"  URL: \033[4;34m{item['url']}\033[0m")
    if item.get('careers_url'):
        print(f"  Careers: \033[4;32m{item['careers_url']}\033[0m")
    if item.get('description'):
        print(f"  Info: {item['description']}")
    if item.get('category'):
        print(f"  Category: {item['category']}")

def main():
    parser = argparse.ArgumentParser(description="Query the Scored Remote Work Ecosystem Master Database")
    parser.add_argument('-s', '--search', help="Search keyword across title, description, and tags")
    parser.add_argument('-t', '--tag', help="Filter by specific tag (e.g. 'AI/ML', 'DevOps/Cloud', '4-Day Week', 'Web3/Crypto')")
    parser.add_argument('-c', '--category', help="Filter by section / category (e.g. 'Job boards', 'Companies with \"remote DNA\"', 'Tools')")
    parser.add_argument('--companies', action='store_true', help="List companies with remote DNA")
    parser.add_argument('--boards', action='store_true', help="List all remote job boards and aggregators")
    parser.add_argument('--tools', action='store_true', help="List all remote collaboration & HR tools")
    parser.add_argument('--tier1', action='store_true', help="Show only Tier 1 Elite / Highest Scoring resources (Score >= 90)")
    parser.add_argument('--stats', action='store_true', help="Print summary statistics of the ecosystem")
    parser.add_argument('--limit', type=int, default=25, help="Max results to display (default: 25, 0 for all)")

    args = parser.parse_args()
    data = load_ecosystem()
    ecosystem = data.get('ecosystem', {})

    if args.stats or len(sys.argv) == 1:
        print("\n=======================================================")
        print("       AWESOME REMOTE WORK ECOSYSTEM INTELLIGENCE      ")
        print("=======================================================")
        meta = data.get('metadata', {})
        print(f"Total Resources Indexed & Scored: {meta.get('total_items', 0)}")
        print(f"Scoring Methodology: {meta.get('scoring_methodology', 'N/A')}")
        print("\nBreakdown by Category:")
        for section, count in meta.get('section_counts', {}).items():
            if count > 0:
                print(f"  • {section:<32}: {count:>3} items")
        print("\nAvailable Tags:")
        tags_set = set()
        for sec, items in ecosystem.items():
            for it in items:
                tags_set.update(it.get('tags', []))
        print("  " + ", ".join(sorted(list(tags_set))))
        print("=======================================================\n")
        if len(sys.argv) == 1:
            print("Tip: Run with --help to see query filters (e.g. --tier1, --search AI, --tag '4-Day Week', --companies)\n")
            return

    candidates = []
    if args.companies:
        candidates.extend(ecosystem.get('Companies with "remote DNA"', []))
    elif args.boards:
        candidates.extend(ecosystem.get('Job boards', []))
        candidates.extend(ecosystem.get('Job boards aggregators', []))
    elif args.tools:
        candidates.extend(ecosystem.get('Tools', []))
    elif args.category:
        for sec, items in ecosystem.items():
            if args.category.lower() in sec.lower():
                candidates.extend(items)
    else:
        for sec, items in ecosystem.items():
            candidates.extend(items)

    results = []
    for item in candidates:
        match = True
        scoring = item.get('scoring', {})
        score = scoring.get('composite_score', 0)

        if args.tier1 and score < 90.0:
            match = False

        if args.search:
            kw = args.search.lower()
            text = f"{item['title']} {item.get('description', '')} {' '.join(item.get('tags', []))}".lower()
            if kw not in text:
                match = False

        if args.tag:
            tag_kw = args.tag.lower()
            item_tags = [t.lower() for t in item.get('tags', [])]
            if not any(tag_kw in t for t in item_tags):
                match = False

        if match:
            results.append(item)

    # Sort results by composite score descending
    results.sort(key=lambda x: x.get('scoring', {}).get('composite_score', 0), reverse=True)

    print(f"\nFound {len(results)} matching scored resources:")
    limit = args.limit if args.limit > 0 else len(results)
    for i, it in enumerate(results[:limit], 1):
        print_item(it, idx=i)

    if len(results) > limit:
        print(f"\n... and {len(results) - limit} more. Use --limit 0 to display all.")

if __name__ == '__main__':
    main()
