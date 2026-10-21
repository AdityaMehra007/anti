import csv
import json

conns = []
try:
    with open('data/Connections_clean.csv', 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            comp = row.get('company', '').strip()
            if 'kpmg' in comp.lower():
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
except Exception as e:
    print(f"Error reading connections: {e}")

print(f"Total KPMG LinkedIn Connections: {len(conns)}")

recruiters = [c for c in conns if c['is_recruiter'] == '1' or any(k in c['position'].lower() for k in ['hr', 'talent', 'recruiter', 'ta '])]
decision_makers = [c for c in conns if c['is_decision_maker'] == '1' or any(k in c['position'].lower() for k in ['manager', 'director', 'lead', 'head', 'vp', 'partner', 'associate director'])]
associates = [c for c in conns if c not in recruiters and c not in decision_makers]

print(f"Recruiters / Talent Acquisition: {len(recruiters)}")
print(f"Managers / Decision Makers / Leaders: {len(decision_makers)}")
print(f"Analysts / Associates / Peers: {len(associates)}")

with open('aditya_kpmg_linkedin_connections.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total': len(conns),
        'recruiters': recruiters,
        'decision_makers': decision_makers,
        'associates': associates,
        'all': conns
    }, f, indent=2)
print("Saved to aditya_kpmg_linkedin_connections.json")
