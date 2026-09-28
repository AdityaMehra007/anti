import os
import json
import re

def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    profile_path = os.path.join(base_dir, 'candidate_profile.json')
    pref_path = os.path.join(base_dir, 'candidate_search_preferences.json')
    eco_path = os.path.join(base_dir, '..', 'remote-resources', 'remote_ecosystem_master.json')

    with open(profile_path, 'r', encoding='utf-8') as f:
        profile = json.load(f)
    with open(pref_path, 'r', encoding='utf-8') as f:
        prefs = json.load(f)
    with open(eco_path, 'r', encoding='utf-8') as f:
        eco = json.load(f)

    return profile, prefs, eco

def score_company(company, profile, prefs):
    name = company['title']
    desc = company.get('description', '').lower()
    raw = company.get('raw', '').lower()
    tags = [t.lower() for t in company.get('tags', [])]
    
    score = 8.0 # Base score for being verified remote DNA
    role_fit = "Business Operations Analyst"
    matched_skills = []
    
    # Check for AI / Data operations fit
    if any(k in desc or k in raw for k in ['ai', 'machine learning', 'data', 'speech', 'vision', 'training', 'annotation', 'eval']):
        score += 1.2
        role_fit = "AI Data Operations & Quality Specialist"
        matched_skills.extend(["Instawork AI Data Curation", "Dataset Quality & Annotation", "Human-in-the-Loop Evaluation"])
        
    # Check for BizOps / Generalist / Scaled operations
    if any(k in desc or k in raw for k in ['operations', 'platform', 'infrastructure', 'remote-first', 'support', 'management', 'workflow']):
        score += 1.0
        if role_fit == "Business Operations Analyst":
            matched_skills.extend(["Operations Leadership (300+ Events)", "Vendor Negotiation (-15% Cost)", "Process Optimization"])

    # Check for B2B / Sales / SaaS / Revenue
    if any(k in desc or k in raw for k in ['b2b', 'sales', 'marketing', 'crm', 'enterprise', 'commerce', 'business', 'growth']):
        score += 0.9
        if "Business Development" not in role_fit and score > 9.2:
            role_fit = "B2B Business Development / Operations Specialist"
        matched_skills.extend(["B2B Lead Generation & Closing", "Enterprise Sales Operations", "Client Retention"])

    # Check for Async / Global remote culture
    if any(k in desc or k in raw for k in ['distributed', '100% remote', 'remote dna', 'worldwide', 'anywhere', 'async']):
        score += 0.6
        matched_skills.append("Async Remote Collaboration Mastery")

    score = min(round(score, 1), 9.9)
    if not matched_skills:
        matched_skills = ["Operations Coordination", "Cross-Border Business Development", "Vendor Management"]

    return score, role_fit, list(set(matched_skills))

def main():
    profile, prefs, eco = load_data()
    companies = eco['ecosystem'].get('Companies with "remote DNA"', [])
    job_boards = eco['ecosystem'].get('Job boards', []) + eco['ecosystem'].get('Job boards aggregators', [])

    scored_companies = []
    for c in companies:
        fit_score, target_role, skills = score_company(c, profile, prefs)
        if fit_score >= 9.0:
            scored_companies.append({
                "company_name": c['title'],
                "website": c['url'],
                "careers_url": c.get('careers_url') or c['url'],
                "target_role": target_role,
                "fit_score": fit_score,
                "fit_band": "9.5 - 10.0 (Elite Fit)" if fit_score >= 9.5 else "9.0 - 9.4 (Strong Fit)",
                "target_compensation_usd": "$45,000 - $70,000 / yr" if fit_score >= 9.5 else "$35,000 - $55,000 / yr",
                "target_compensation_inr_equiv": "INR 38L - 58L LPA" if fit_score >= 9.5 else "INR 29L - 46L LPA",
                "matched_skills": skills,
                "company_description": c.get('description', ''),
                "action_priority": "Tier 1: Priority Direct Application" if fit_score >= 9.6 else "Tier 2: Active Pipeline"
            })

    # Sort by fit_score descending
    scored_companies.sort(key=lambda x: x['fit_score'], reverse=True)

    # Filter top job boards for Aditya's profile
    targeted_boards = []
    for b in job_boards:
        text = f"{b['title']} {b.get('description', '')}".lower()
        if any(k in text for k in ['ai', 'data', '4 day', 'operation', 'sales', 'business', 'latam', 'general', 'worldwide', 'anywhere', 'remotive', 'weworkremotely']):
            targeted_boards.append({
                "board_name": b['title'],
                "url": b['url'],
                "tags": b.get('tags', []),
                "description": b.get('description', '')
            })

    output_data = {
        "candidate": {
            "name": profile['full_name'],
            "headline": profile['headline'],
            "verified_anchors": prefs['candidate']['verified_truth_base'],
            "location": f"{profile['location']['city']}, {profile['location']['country']}"
        },
        "total_remote_companies_evaluated": len(companies),
        "total_high_fit_companies": len(scored_companies),
        "tier_1_priority_count": sum(1 for c in scored_companies if c['fit_score'] >= 9.6),
        "matched_companies": scored_companies,
        "recommended_niche_boards": targeted_boards[:15]
    }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'remote_matched_opportunities.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Evaluated {len(companies)} companies.")
    print(f"Found {len(scored_companies)} high-fit remote companies for Aditya Mehra.")
    print(f"Tier 1 Priority: {output_data['tier_1_priority_count']} companies.")
    print(f"Saved matched opportunities to: {out_path}")

if __name__ == '__main__':
    main()
