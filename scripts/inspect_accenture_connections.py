import csv
import json

conns = []
with open('data/Connections_clean.csv', 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        comp = row.get('company', '').strip()
        if 'accenture' in comp.lower():
            conns.append({
                'id': row.get('id'),
                'name': row.get('full_name') or f"{row.get('first_name')} {row.get('last_name')}".strip(),
                'company': comp,
                'position': row.get('position', '').strip(),
                'department': row.get('department', '').strip(),
                'seniority': row.get('seniority', '').strip(),
                'url': row.get('url', '').strip(),
                'connected_on': row.get('connected_on', '').strip(),
                'is_recruiter': row.get('is_recruiter', '0'),
                'is_decision_maker': row.get('is_decision_maker', '0')
            })

print(f"Total Accenture LinkedIn Connections: {len(conns)}")

recruiters = [c for c in conns if c['is_recruiter'] == '1' or 'hr' in c['position'].lower() or 'talent' in c['position'].lower() or 'recruiter' in c['position'].lower()]
operations = [c for c in conns if any(w in c['position'].lower() for w in ['operations', 'procurement', 'supply', 'associate', 'analyst', 'order', 'p2p'])]
managers = [c for c in conns if any(w in c['position'].lower() for w in ['manager', 'lead', 'head', 'director', 'vice president', 'vp'])]

print(f"\n--- RECRUITERS & HR TALENT ACQUISITION ({len(recruiters)}) ---")
for i, c in enumerate(recruiters, 1):
    print(f"{i:2d}. {c['name']} | {c['position']} | Connected: {c['connected_on']}")
    print(f"    URL: {c['url']}")

print(f"\n--- OPERATIONS & ASSOCIATES / PEERS ({len(operations)}) ---")
for i, c in enumerate(operations[:25], 1):
    print(f"{i:2d}. {c['name']} | {c['position']} | Connected: {c['connected_on']}")
    print(f"    URL: {c['url']}")

print(f"\n--- MANAGERS & DECISION MAKERS ({len(managers)}) ---")
for i, c in enumerate(managers[:25], 1):
    print(f"{i:2d}. {c['name']} | {c['position']} | Connected: {c['connected_on']}")
    print(f"    URL: {c['url']}")

with open('aditya_accenture_linkedin_connections.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total': len(conns),
        'recruiters': recruiters,
        'operations': operations,
        'managers': managers,
        'all': conns
    }, f, indent=2)
