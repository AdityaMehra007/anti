import json

with open(r'e:\anti\teamwork_projects\bangalore_referral_strike\bangalore_live_referral_dockets.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

corridor_groups = {
    'ORR': [],
    'Manyata': [],
    'Bellandur': [],
    'Whitefield': [],
    'Domlur': [],
    'Other / Central': []
}

for item in data:
    c = item.get('corridor', '')
    comp = item.get('canonical_company', '')
    clow = c.lower()
    
    matched = False
    if 'bellandur' in clow:
        corridor_groups['Bellandur'].append((comp, c))
        matched = True
    if 'outer ring road' in clow or 'orr' in clow:
        corridor_groups['ORR'].append((comp, c))
        matched = True
    if 'manyata' in clow or 'hebbal' in clow:
        corridor_groups['Manyata'].append((comp, c))
        matched = True
    if 'whitefield' in clow:
        corridor_groups['Whitefield'].append((comp, c))
        matched = True
    if 'domlur' in clow or 'intermediate ring road' in clow:
        corridor_groups['Domlur'].append((comp, c))
        matched = True
    if not matched:
        corridor_groups['Other / Central'].append((comp, c))

for k, v in corridor_groups.items():
    print(f"\n=== Corridor Pill: {k} ({len(v)} companies) ===")
    for comp, c in v:
        print(f"  {comp} -> {c}")
