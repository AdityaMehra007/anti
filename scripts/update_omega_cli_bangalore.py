import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cli_path = os.path.join(REPO_ROOT, "omega_cli.py")

with open(cli_path, "r", encoding="utf-8") as f:
    content = f.read()

start_mark = "def cmd_bangalore(args):"
end_mark = "def cmd_deals(args):"

idx1 = content.find(start_mark)
idx2 = content.find(end_mark)

if idx1 == -1 or idx2 == -1:
    print(f"Error: indices not found ({idx1}, {idx2})")
    sys.exit(1)

new_cmd_bangalore = '''def cmd_bangalore(args):
    """Inspect Bangalore Top 500 Startups, Prompts, Scaffolds, and Flagship Codebases."""
    master_json_path = os.path.join(REPO_ROOT, "data", "BANGALORE_TOP_500_STARTUPS_PROJECTS_PROMPTS_MASTER.json")
    if not os.path.exists(master_json_path):
        print(f"[ERROR] Master JSON not found at {master_json_path}")
        return

    with open(master_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    startups = data if isinstance(data, list) else data.get("startups", [])
    query = getattr(args, "search", None)
    inspect_name = getattr(args, "inspect", None)

    print("=" * 76)
    print("  OMEGA INFINITY - BENGALURU TOP 500 STARTUPS & FLAGSHIP ARCHITECTURE")
    print("=" * 76)

    if inspect_name:
        match = next((s for s in startups if inspect_name.lower() in s.get("company_name", "").lower()), None)
        if not match:
            print(f"[NOT FOUND] No startup matching '{inspect_name}'")
        else:
            proj = match.get("biggest_project", {})
            prompt = match.get("biggest_prompt", "")
            print(f"Startup Name     : {match.get('company_name', '')} (Rank #{match.get('rank', 'N/A')})")
            print(f"Sector / Stage   : {match.get('sector', 'N/A')} | Stage: {match.get('stage', 'N/A')}")
            print(f"Valuation/Funding: {match.get('valuation_or_funding', 'N/A')}")
            print(f"Tech Corridor    : {match.get('corridor', 'Bengaluru Core')}")
            print(f"Flagship Project : {proj.get('project_name', 'N/A')}")
            print(f"Strategic Thesis : {proj.get('strategic_thesis', 'N/A')}")
            print(f"Architecture     : {proj.get('architecture_pillar', 'N/A')}")
            print(f"Tech Stack       : {', '.join(proj.get('tech_stack', []))}")
            print(f"Prompt Length    : {len(prompt):,} characters (~{len(prompt)//4:,} tokens)")
            print("-" * 76)
            print("MASTER SOVEREIGN PROMPT PREVIEW (FIRST 400 CHARS):")
            print(prompt[:400] + "...")
        print("=" * 76)
        return

    if query:
        matches = [s for s in startups if query.lower() in s.get("company_name", "").lower() or query.lower() in s.get("sector", "").lower() or query.lower() in s.get("biggest_project", {}).get("project_name", "").lower()]
        print(f"Search Query     : '{query}' -> Found {len(matches)} matching startups")
        print("-" * 76)
        print(f"{'RANK':<6} | {'COMPANY NAME':<24} | {'SECTOR':<20} | {'FLAGSHIP PROJECT'}")
        print("-" * 76)
        for s in matches[:15]:
            p_name = s.get("biggest_project", {}).get("project_name", "")
            short_p = (p_name[:32] + "..") if len(p_name) > 34 else p_name
            print(f"#{s.get('rank', 0):<5} | {s.get('company_name', ''):<24} | {s.get('sector', ''):<20} | {short_p}")
        if len(matches) > 15:
            print(f"  ... and {len(matches) - 15} more matches.")
        print("=" * 76)
        return

    # Default: summary stats
    sectors = {}
    for s in startups:
        sec = s.get("sector", "Other")
        sectors[sec] = sectors.get(sec, 0) + 1

    total_prompt_chars = sum(len(s.get("biggest_prompt", "")) for s in startups)

    print(f"Total Startups Cataloged  : {len(startups)}")
    print(f"Master System Prompts     : 500 Deep Prompts ({total_prompt_chars:,} chars / ~{total_prompt_chars//4:,} tokens)")
    print(f"Modular Code Scaffolds    : 2,500 Production Files (5 files/startup across 500 dirs)")
    print(f"Concrete Flagship Systems : 10 Production Systems (Razorpay, Zerodha, Swiggy, Flipkart, etc.)")
    print(f"Cockpit Dashboard UI      : bangalore_top_500_cockpit.html (10,000 TPS Simulator)")
    print("-" * 76)
    print("SECTOR BREAKDOWN:")
    for sec, count in sorted(sectors.items(), key=lambda x: x[1], reverse=True)[:8]:
        bar = "#" * (count // 2)
        print(f"  * {sec:<24}: {count:>3} startups {bar}")
    print("=" * 76)


'''

content = content[:idx1] + new_cmd_bangalore + content[idx2:]

with open(cli_path, "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] omega_cli.py updated successfully!")
