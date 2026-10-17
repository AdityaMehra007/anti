import csv
import json
import sys

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

conns = []
with open('data/Connections_clean.csv', 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        comp = row.get('company', '').strip()
        if 'accenture' in comp.lower():
            # Clean non-ascii
            name = (row.get('full_name') or f"{row.get('first_name')} {row.get('last_name')}").encode('ascii', 'ignore').decode('ascii').strip()
            pos = (row.get('position', '')).encode('ascii', 'ignore').decode('ascii').strip()
            conns.append({
                'id': row.get('id'),
                'name': name,
                'company': comp,
                'position': pos,
                'department': row.get('department', '').strip(),
                'seniority': row.get('seniority', '').strip(),
                'url': row.get('url', '').strip(),
                'connected_on': row.get('connected_on', '').strip(),
                'is_recruiter': row.get('is_recruiter', '0'),
                'is_decision_maker': row.get('is_decision_maker', '0')
            })

print(f"Total Accenture Connections: {len(conns)}")

# Categorize into key buckets
recruiters = [c for c in conns if c['is_recruiter'] == '1' or any(w in c['position'].lower() for w in ['hr', 'talent', 'recruiter', 'recruiting', 'talent acquisition'])]
procurement_ops = [c for c in conns if any(w in c['position'].lower() for w in ['procurement', 'supply', 'order', 'sourcing', 'logistics'])]
general_ops = [c for c in conns if any(w in c['position'].lower() for w in ['operations', 'associate', 'analyst', 'trust', 'compliance', 'business advisory']) and c not in recruiters and c not in procurement_ops]
leadership = [c for c in conns if any(w in c['position'].lower() for w in ['manager', 'lead', 'head', 'director', 'vp']) and c not in recruiters]

with open('aditya_accenture_linkedin_network.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total': len(conns),
        'recruiters': recruiters,
        'procurement_and_supply_chain': procurement_ops,
        'general_operations_and_analysts': general_ops,
        'leadership_and_managers': leadership,
        'all': conns
    }, f, indent=2)

print(f"Recruiters & Talent Acquisition: {len(recruiters)}")
print(f"Procurement & Supply Chain / Order Ops: {len(procurement_ops)}")
print(f"General Operations & Analysts: {len(general_ops)}")
print(f"Leadership & Managers: {len(leadership)}")
