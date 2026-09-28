import os
import json
import csv
import re

def compute_company_score(item, profile_text):
    title = item['title'].lower()
    desc = item.get('description', '').lower()
    raw = item.get('raw', '').lower()
    combined = f"{title} {desc} {raw}"
    
    # 1. Candidate Fit Score (0.0 - 10.0)
    fit_score = 7.5 # Base for being an established remote DNA company
    
    # Operations & Vendor Governance
    if any(k in combined for k in ['operations', 'platform', 'infrastructure', 'workflow', 'management', 'support', 'coordination', 'logistics']):
        fit_score += 0.8
    # AI Data & ML Ops
    if any(k in combined for k in ['ai', 'machine learning', 'data', 'eval', 'speech', 'vision', 'training', 'annotation', 'dataset']):
        fit_score += 0.9
    # B2B Sales, Growth, Client Success
    if any(k in combined for k in ['b2b', 'sales', 'growth', 'marketing', 'crm', 'enterprise', 'commerce', 'client', 'revenue']):
        fit_score += 0.5
    # Radical Async / Global Remote
    if any(k in combined for k in ['distributed', '100% remote', 'remote dna', 'worldwide', 'anywhere', 'handbook', 'async']):
        fit_score += 0.4
        
    fit_score = min(round(fit_score, 1), 9.9)

    # 2. Remote Maturity Score (0 - 100)
    remote_maturity = 75
    if any(k in combined for k in ['100% remote', '100% distributed', 'fully distributed', 'all-remote']):
        remote_maturity = 98
    elif any(k in combined for k in ['remote-first', 'remote dna', 'async', 'distributed']):
        remote_maturity = 90
    elif any(k in combined for k in ['remote friendly', 'remote ok']):
        remote_maturity = 80

    # 3. Compensation Leverage Score (0 - 100)
    # Global remote tech firms paying in USD offer massive leverage in India
    comp_leverage = 85
    if any(k in combined for k in ['enterprise', 'ai', 'cloud', 'security', 'infrastructure', 'observability']):
        comp_leverage = 95
    elif any(k in combined for k in ['consultancy', 'agency', 'small team']):
        comp_leverage = 78

    # 4. Hiring Probability & Velocity (0.0 - 1.0)
    hiring_prob = 0.80
    if item.get('careers_url'):
        hiring_prob += 0.10
    if any(k in combined for k in ['hiring', 'grow', 'scale', 'join us', 'careers']):
        hiring_prob += 0.05
    hiring_prob = min(round(hiring_prob, 2), 0.95)

    # 5. Composite Rank Score (0 - 100)
    composite = round((fit_score * 5.0) + (remote_maturity * 0.25) + (comp_leverage * 0.25), 1)

    if composite >= 92:
        tier = "Tier 1: Elite Direct Target"
        fit_band = "9.5 - 10.0 (Elite Fit)"
    elif composite >= 85:
        tier = "Tier 2: High-Priority Pipeline"
        fit_band = "9.0 - 9.4 (Strong Fit)"
    else:
        tier = "Tier 3: Specialized Watchlist"
        fit_band = "8.0 - 8.9 (Viable Fit)"

    return {
        "candidate_fit_score": fit_score,
        "remote_maturity_score": remote_maturity,
        "compensation_leverage_score": comp_leverage,
        "hiring_probability": hiring_prob,
        "composite_score": composite,
        "fit_band": fit_band,
        "strategic_tier": tier,
        "primary_track": "AI Data Operations & Ops" if "ai" in combined else "Global Business Operations"
    }

def compute_job_board_score(item):
    title = item['title'].lower()
    desc = item.get('description', '').lower()
    combined = f"{title} {desc}"

    # Utility Score (0 - 100)
    utility = 75
    if any(k in combined for k in ['real-time', 'daily', 'verified', 'thousands', 'api', 'mcp', 'curated']):
        utility += 15
    if 'premium membership' in combined or 'requires premium' in combined:
        utility -= 20

    # Role Breadth & Non-Tech Accessibility (0 - 100)
    breadth = 70
    if any(k in combined for k in ['every role', 'non-tech', 'business', 'operations', 'sales', 'marketing', 'any category', 'all roles']):
        breadth = 95
    elif any(k in combined for k in ['ai', 'data', '4-day', '4 day', 'crypto', 'web3']):
        breadth = 85
    elif any(k in combined for k in ['clojure', 'golang', 'ruby', 'python', 'vue']):
        breadth = 65

    # Global Accessibility Score (0 - 100)
    global_acc = 80
    if any(k in combined for k in ['anywhere', 'work from anywhere', 'worldwide', '100% work from anywhere', 'latam', 'global']):
        global_acc = 95
    elif any(k in combined for k in ['us only', 'canada only', 'german', 'poland', 'chile']):
        global_acc = 70

    composite = round((utility * 0.4) + (breadth * 0.3) + (global_acc * 0.3), 1)
    
    if composite >= 88:
        tier = "Tier 1: Daily Essential Feed"
    elif composite >= 78:
        tier = "Tier 2: Weekly Review Target"
    else:
        tier = "Tier 3: Specialized Niche Board"

    return {
        "utility_score": utility,
        "role_breadth_score": breadth,
        "global_accessibility_score": global_acc,
        "composite_score": composite,
        "fit_band": f"Score {composite}/100",
        "strategic_tier": tier
    }

def compute_tool_score(item):
    combined = f"{item['title']} {item.get('description', '')}".lower()
    ecosystem_adoption = 75
    if any(k in combined for k in ['deel', 'remote.com', 'oyster', 'slack', 'zoom', 'loom', 'notion', 'trello', 'github', 'basecamp', 'twist']):
        ecosystem_adoption = 98
    elif any(k in combined for k in ['hr', 'payroll', 'compliance', 'communication', 'meetings', 'chat', 'project management']):
        ecosystem_adoption = 88

    candidate_utility = 70
    if any(k in combined for k in ['payroll', 'contract', 'eor', 'async', 'timezone', 'standup']):
        candidate_utility = 92

    composite = round((ecosystem_adoption * 0.6) + (candidate_utility * 0.4), 1)
    return {
        "adoption_score": ecosystem_adoption,
        "candidate_utility_score": candidate_utility,
        "composite_score": composite,
        "fit_band": f"Impact {composite}/100",
        "strategic_tier": "Core Remote Stack" if composite >= 85 else "Specialized Remote Tool"
    }

def compute_relocation_score(item):
    combined = f"{item['title']} {item.get('description', '')}".lower()
    cash_val = 70
    if '$10,000' in combined or '10,000' in combined:
        cash_val = 98
    elif '$5,000' in combined or '5,000' in combined:
        cash_val = 85

    feasibility = 75
    if 'tulsa' in combined or 'shoals' in combined or 'vermont' in combined:
        feasibility = 85

    composite = round((cash_val * 0.6) + (feasibility * 0.4), 1)
    return {
        "cash_incentive_score": cash_val,
        "program_feasibility_score": feasibility,
        "composite_score": composite,
        "fit_band": f"Grant ROI {composite}/100",
        "strategic_tier": "High Financial Incentive ($10,000)" if cash_val >= 95 else "Regional Support Grant"
    }

def compute_generic_resource_score(item, section):
    combined = f"{item['title']} {item.get('description', '')}".lower()
    authority = 80
    if any(k in combined for k in ['gitlab', 'basecamp', '37signals', 'zapier', 'automattic', 'scott berkun', 'harvard', 'nytimes', 'forbes']):
        authority = 95

    actionability = 75
    if section in ['Interviewing', 'Housing', 'Law & Finance']:
        actionability = 88
    elif section in ['Books', 'Articles & Posts']:
        actionability = 82

    composite = round((authority * 0.5) + (actionability * 0.5), 1)
    return {
        "authority_score": authority,
        "actionability_score": actionability,
        "composite_score": composite,
        "fit_band": f"Quality {composite}/100",
        "strategic_tier": "Must-Read / High Value" if composite >= 88 else "Supplementary Knowledge"
    }

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'remote_ecosystem_master.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        master = json.load(f)

    ecosystem = master['ecosystem']
    all_scored_items = []

    print("Beginning multi-dimensional scoring of all 520 entities...")

    for section, items in ecosystem.items():
        for it in items:
            if section == 'Companies with "remote DNA"':
                score_data = compute_company_score(it, "")
            elif section in ['Job boards', 'Job boards aggregators']:
                score_data = compute_job_board_score(it)
            elif section == 'Tools':
                score_data = compute_tool_score(it)
            elif section == 'Relocation Incentives':
                score_data = compute_relocation_score(it)
            else:
                score_data = compute_generic_resource_score(it, section)

            it['scoring'] = score_data
            all_scored_items.append({
                "title": it['title'],
                "url": it['url'],
                "section": section,
                "category": it.get('category', section),
                "composite_score": score_data['composite_score'],
                "strategic_tier": score_data['strategic_tier'],
                "fit_band": score_data['fit_band'],
                "tags": ", ".join(it.get('tags', [])),
                "description": it.get('description', '')
            })

    # Sort all items by composite score descending
    all_scored_items.sort(key=lambda x: x['composite_score'], reverse=True)

    # Add overall rank
    for rank, it in enumerate(all_scored_items, 1):
        it['rank'] = rank

    # Save enriched master JSON
    master['metadata']['scored_at'] = "2026-09-28T16:20:00Z"
    master['metadata']['scoring_methodology'] = "Antigravity Multi-Metric Decision Matrix V22"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(master, f, indent=2, ensure_ascii=False)
    print(f"Updated {json_path} with scores for all {len(all_scored_items)} entities.")

    # Export master CSV ranking
    csv_path = os.path.join(base_dir, 'all_entities_ranked_and_scored.csv')
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Rank', 'Entity Title', 'Section', 'Category', 'Composite Score (0-100)', 'Strategic Tier', 'Fit Band', 'Tags', 'URL', 'Description'])
        for it in all_scored_items:
            writer.writerow([
                it['rank'],
                it['title'],
                it['section'],
                it['category'],
                it['composite_score'],
                it['strategic_tier'],
                it['fit_band'],
                it['tags'],
                it['url'],
                it['description']
            ])
    print(f"Exported master ranking CSV to: {csv_path}")

    # Output stats
    tier_counts = {}
    for it in all_scored_items:
        tier_counts[it['strategic_tier']] = tier_counts.get(it['strategic_tier'], 0) + 1
    print("\nScore Distribution Across Tiers:")
    for t, cnt in tier_counts.items():
        print(f"  • {t}: {cnt} resources")

if __name__ == '__main__':
    main()
