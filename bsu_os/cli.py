"""BSU OS Unified CLI Interface.

Allows running ecosystem operations directly from terminal:
- Seed database: python -m bsu_os.cli seed
- Serve dashboard: python -m bsu_os.cli serve --port 8000
- Run Super Search: python -m bsu_os.cli search "Sarvam"
- Generate Daily Brief: python -m bsu_os.cli brief
- Run Copilot Query: python -m bsu_os.cli query "Where should I open an AI lab in Bengaluru?"
- Recompute Scores: python -m bsu_os.cli score
"""

import sys
import argparse
import json
import uvicorn

from bsu_os.config import DEFAULT_HOST, DEFAULT_PORT
from bsu_os.seed_data import seed_database
from bsu_os.search_engine import super_search
from bsu_os.scoring_engine import recompute_all_scores
from bsu_os.copilot_engine import CopilotEngine
from bsu_os.alerts_engine import generate_daily_brief
from bsu_os.database import get_all_startups


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        prog="bsu_os",
        description="Bengaluru Startup Universe (BSU OS) Unified CLI Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # seed
    subparsers.add_parser("seed", help="Initialize SQLite schema and seed verified ecosystem data")

    # serve
    serve_parser = subparsers.add_parser("serve", help="Launch the BSU OS web dashboard server")
    serve_parser.add_argument("--host", default=DEFAULT_HOST, help="Host address (default 127.0.0.1)")
    serve_parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port (default 8000)")

    # search
    search_parser = subparsers.add_parser("search", help="Execute multi-entity Super Search")
    search_parser.add_argument("query", help="Search keyword or query")

    # brief
    subparsers.add_parser("brief", help="Display Section 204 Daily Ecosystem Briefing")

    # query
    query_parser = subparsers.add_parser("query", help="Ask the Multi-Agent Copilot an ecosystem question")
    query_parser.add_argument("prompt", help="Natural language question")
    query_parser.add_argument("--mode", default="general", help="Specialized agent mode (founder, investor, career, geo)")

    # score
    subparsers.add_parser("score", help="Recalculate Power, Career, and Momentum scores for all startups")

    args = parser.parse_args()

    if args.command == "seed":
        print("[BSU OS] Initializing database and seeding verified ecosystem dataset...")
        seed_database()
        recompute_all_scores()
        print("[BSU OS] Successfully seeded Bengaluru tech entities, clusters, and jobs.")

    elif args.command == "serve":
        print(f"[BSU OS] Starting server on http://{args.host}:{args.port}")
        uvicorn.run("bsu_os.server:app", host=args.host, port=args.port, reload=False)

    elif args.command == "search":
        print(f"[BSU OS] Searching ecosystem for: '{args.query}'\n")
        results = super_search(args.query)
        for cat, items in results.items():
            if items:
                print(f"=== {cat.upper()} ({len(items)}) ===")
                for item in items[:5]:
                    name = item.get("name") or item.get("title") or item.get("firm_name")
                    extra = item.get("sector") or item.get("department") or ""
                    print(f" - {name} ({extra})")
                print()

    elif args.command == "brief":
        brief = generate_daily_brief()
        print(f"\n=== BSU OS DAILY INTELLIGENCE BRIEF ({brief['date']}) ===")
        print(f"Theme: {brief['theme']}\n")
        print("⚡ HIGH-IMPACT OPPORTUNITIES:")
        for opp in brief["opportunities"]:
            print(f"  • {opp}")
        print("\n📈 EMERGING TREND:")
        print(f"  {brief['emerging_trend']['title']}: {brief['emerging_trend']['summary']}")
        print("\n🎯 STRATEGIC DIRECTIVES:")
        for act in brief["recommended_actions"]:
            print(f"  • {act}")
        print()

    elif args.command == "query":
        copilot = CopilotEngine()
        print(f"[BSU OS COPILOT] Processing query: '{args.prompt}' (Mode: {args.mode})...\n")
        res = copilot.query(args.prompt, mode=args.mode)
        print(f"💡 VERDICT: {res['verdict']}\n")
        print("🔍 EVIDENCE (Section 197 Ground-Truth):")
        for ev in res["evidence"]:
            print(f"  • {ev}")
        print(f"\n📊 FIT SCORE: {res['fit_score']}/100")
        print(f"🚀 RECOMMENDED ACTION: {res['recommended_action']}")
        print("\n⚠️ RISK FACTORS:")
        for rk in res["risk_factors"]:
            print(f"  • {rk}")
        print()

    elif args.command == "score":
        print("[BSU OS] Recalculating mathematical scores for all startups...")
        cnt = recompute_all_scores()
        print(f"[BSU OS] Done. Recomputed scores for {cnt} startups.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
