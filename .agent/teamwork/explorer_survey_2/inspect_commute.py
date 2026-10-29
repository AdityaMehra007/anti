import json

with open('data/BANGALORE_COMMUTE_EV_MATRIX.json', 'r', encoding='utf-8') as f:
    commute = json.load(f)

targets = ['accenture', 'deloitte', 'goldman', 'amazon', 'ibm', 'jpmorgan', 'jp morgan', 'kpmg', 'pwc', 'walmart', 'delhivery', 'phonepe']

found = {}
for item in commute:
    c = item.get('company', '').lower()
    for t in targets:
        if t in c:
            found.setdefault(t, []).append(item)
            break

print("=== COMMUTE MATRIX FINDINGS ===")
for t, items in found.items():
    print(f"\nTarget: {t.upper()} ({len(items)} entries)")
    # group by corridor
    corrs = {}
    for it in items:
        corr = it.get('corridor')
        corrs.setdefault(corr, []).append(it)
    for corr, l in corrs.items():
        sample = l[0]
        print(f"  Corridor: {corr} (Count: {len(l)}) | Commute: {sample.get('travel_mins')} min | Mode: {sample.get('transit_mode')} | Grade: {sample.get('commute_grade')} | Salary: {sample.get('ctc_min_inr')}-{sample.get('ctc_max_inr')}")
