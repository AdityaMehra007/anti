import json

with open(r'e:\anti\teamwork_projects\bangalore_referral_strike\bangalore_live_referral_dockets.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

domains = {
    'Operations': [],
    'Supply Chain': [],
    'Advisory/Risk': [],
    'Trade Finance': [],
    'Merchant BD': []
}

def classify_job(title):
    t = title.lower()
    if 'trade' in t or 'receivables' in t or 'finance' in t or 'exim' in t:
        return 'Trade Finance'
    if 'risk' in t or 'advisory' in t or 'audit' in t or 'compliance' in t:
        return 'Advisory/Risk'
    if 'supply chain' in t or 'logistics' in t or 'freight' in t or 'procurement' in t or 'vendor' in t:
        return 'Supply Chain'
    if 'merchant' in t or 'business development' in t or 'bd' in t or 'sales' in t or 'brand activation' in t:
        return 'Merchant BD'
    if 'operations' in t or 'ops' in t or 'member experience' in t or 'community' in t or 'support' in t:
        return 'Operations'
    return 'Other'

unmatched = []
for item in data:
    role = item.get('job_title', '')
    comp = item.get('canonical_company', '')
    dom = classify_job(role)
    if dom in domains:
        domains[dom].append((comp, role))
    else:
        unmatched.append((comp, role))

for d, roles in domains.items():
    print(f"\n=== Domain: {d} ({len(roles)} companies) ===")
    for c, r in roles:
        print(f"  - {c}: {r}")

if unmatched:
    print(f"\n=== Unmatched ({len(unmatched)}): ===")
    for c, r in unmatched:
        print(f"  - {c}: {r}")
