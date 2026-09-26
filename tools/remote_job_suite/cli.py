"""
Unified CLI for awesome-remote-job Suite
Explore companies, job boards, remote tools, relocation incentives, and live job postings.
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_json(filename: str) -> List[Dict[str, Any]]:
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"Error: Data file {filename} not found. Run extractor.py first.", file=sys.stderr)
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def cmd_stats(args):
    files = {
        "Companies with Remote DNA": "companies.json",
        "Curated Job Boards": "job_boards.json",
        "Job Aggregators": "job_aggregators.json",
        "Remote Operating Tools": "tools.json",
        "Interviewing Resources": "interviewing.json",
        "Coliving & Housing": "housing.json",
        "Relocation Cash Incentives": "relocation_incentives.json",
        "Podcasts": "podcasts.json",
        "Books": "books.json",
        "Communities": "communities.json",
    }
    print("\n" + "=" * 55)
    print("      AWESOME REMOTE JOB — REPOSITORY METRICS")
    print("=" * 55)
    total = 0
    for label, fname in files.items():
        data = load_json(fname)
        print(f"  {label:<30} : {len(data):4d} items")
        total += len(data)
    print("-" * 55)
    print(f"  {'TOTAL CURATED ASSETS':<30} : {total:4d} entries")
    print("=" * 55 + "\n")


def cmd_companies(args):
    companies = load_json("companies.json")
    query = (args.query or "").lower()
    tag = (args.tag or "").lower()

    filtered = []
    for c in companies:
        name = c.get("name", "")
        desc = c.get("description", "")
        tags = [t.lower() for t in c.get("tags", [])]

        if tag and tag not in tags:
            continue
        if query and (query not in name.lower() and query not in desc.lower()):
            continue
        filtered.append(c)

    print(f"\nFound {len(filtered)} remote-DNA companies matching criteria:")
    print("-" * 80)
    for c in filtered[:args.limit]:
        tags_str = f"[{', '.join(c.get('tags', []))}]"
        print(f"• {c['name']} {tags_str}")
        print(f"  Careers: {c['url']}")
        if c.get("description"):
            print(f"  Details: {c['description']}")
        print()

    if len(filtered) > args.limit:
        print(f"... and {len(filtered) - args.limit} more companies. Use --limit to show more.\n")


def cmd_boards(args):
    boards = load_json("job_boards.json")
    aggregators = load_json("job_aggregators.json")
    all_boards = boards + aggregators
    category = (args.category or "").lower()
    query = (args.query or "").lower()

    filtered = []
    for b in all_boards:
        name = b.get("name", "")
        desc = b.get("description", "")
        tags = [t.lower() for t in b.get("tags", [])]

        if category and category not in tags:
            continue
        if query and (query not in name.lower() and query not in desc.lower()):
            continue
        filtered.append(b)

    print(f"\nFound {len(filtered)} curated job boards & aggregators:")
    print("-" * 80)
    for b in filtered[:args.limit]:
        tags_str = f"[{', '.join(b.get('tags', []))}]"
        print(f"• {b['name']} {tags_str}")
        print(f"  URL: {b['url']}")
        if b.get("description"):
            print(f"  Focus: {b['description']}")
        print()


def cmd_incentives(args):
    incentives = load_json("relocation_incentives.json")
    print("\n" + "=" * 70)
    print("      REMOTE WORK RELOCATION INCENTIVES & GRANTS")
    print("=" * 70)
    for inc in incentives:
        print(f"\n• {inc['name']}")
        print(f"  URL: {inc['url']}")
        print(f"  Terms: {inc['description']}")
    print("\n" + "=" * 70 + "\n")


def cmd_tools(args):
    tools = load_json("tools.json")
    query = (args.query or "").lower()
    filtered = [t for t in tools if not query or query in t['name'].lower() or query in t['description'].lower()]
    print(f"\nFound {len(filtered)} remote team tools:")
    print("-" * 75)
    for t in filtered[:args.limit]:
        print(f"• {t['name']}")
        print(f"  URL: {t['url']}")
        if t.get("description"):
            print(f"  Description: {t['description']}")
        print()


def cmd_live(args):
    # Delegate to scraper
    from scraper import search_all_jobs, format_markdown
    jobs = search_all_jobs(keyword=args.keyword, limit_per_source=args.limit)
    if args.markdown:
        print(format_markdown(jobs, args.keyword))
    else:
        print(f"\n{'TITLE':<40} | {'COMPANY':<20} | {'LOCATION':<18} | {'SOURCE':<10}")
        print("-" * 94)
        for j in jobs:
            print(f"{j['title'][:38]:<40} | {j['company'][:18]:<20} | {j['location'][:16]:<18} | {j['source']:<10}")
            print(f"  Link: {j['url']}")
        print(f"\nTotal fetched: {len(jobs)} jobs\n")


def main():
    parser = argparse.ArgumentParser(description="Awesome Remote Job CLI Suite")
    subparsers = parser.add_subparsers(dest="command")

    # stats
    subparsers.add_parser("stats", help="Display overview summary metrics")

    # companies
    p_comp = subparsers.add_parser("companies", help="Query companies with remote DNA")
    p_comp.add_argument("-q", "--query", help="Keyword search in name/description")
    p_comp.add_argument("-t", "--tag", help="Filter by tag (ai, devtools, cloud-infra, fintech-web3, saas, design)")
    p_comp.add_argument("-l", "--limit", type=int, default=15, help="Number of results to display")

    # boards
    p_boards = subparsers.add_parser("boards", help="Browse curated job boards & aggregators")
    p_boards.add_argument("-c", "--category", help="Category (ai-ml, python, golang, javascript, backend, web3-crypto, regional-latam, flexible-4day)")
    p_boards.add_argument("-q", "--query", help="Keyword search")
    p_boards.add_argument("-l", "--limit", type=int, default=15, help="Number of results to display")

    # incentives
    subparsers.add_parser("incentives", help="View relocation cash grants and incentives")

    # tools
    p_tools = subparsers.add_parser("tools", help="Browse remote collaboration and HR tools")
    p_tools.add_argument("-q", "--query", help="Search query")
    p_tools.add_argument("-l", "--limit", type=int, default=15, help="Number of results")

    # live
    p_live = subparsers.add_parser("live", help="Search real-time active job openings")
    p_live.add_argument("-k", "--keyword", help="Search term (e.g. ai, python, react, rust)")
    p_live.add_argument("-l", "--limit", type=int, default=10, help="Limit per source")
    p_live.add_argument("--markdown", action="store_true", help="Format as markdown table")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    cmds = {
        "stats": cmd_stats,
        "companies": cmd_companies,
        "boards": cmd_boards,
        "incentives": cmd_incentives,
        "tools": cmd_tools,
        "live": cmd_live
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
