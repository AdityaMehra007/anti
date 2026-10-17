import csv
import json
import sqlite3
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

all_people = {}

# 1. From Connections_clean.csv (Aditya's 1st-degree LinkedIn connections)
csv_path = os.path.join('data', 'Connections_clean.csv')
if os.path.exists(csv_path):
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for r in reader:
            comp = r.get('company', '').strip()
            if 'accenture' in comp.lower():
                name = r.get('full_name') or f"{r.get('first_name', '')} {r.get('last_name', '')}".strip()
                url = r.get('url', '').strip()
                pos = r.get('position', '').strip()
                key = url if url else name.lower()
                all_people[key] = {
                    'name': name,
                    'title': pos,
                    'company': comp,
                    'url': url,
                    'connected_on': r.get('connected_on', ''),
                    'source': 'LinkedIn 1st-Degree Connection',
                    'is_recruiter': r.get('is_recruiter', '0'),
                    'is_decision_maker': r.get('is_decision_maker', '0')
                }

# 2. From aditya_global_career_intelligence.db
db_path = os.path.join('data', 'aditya_global_career_intelligence.db')
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT full_name, current_title, company_name, linkedin_url, classification, professional_email, public_business_phone FROM people WHERE LOWER(company_name) LIKE '%accenture%'")
    for row in cur.fetchall():
        name, title, comp, url, classification, email, phone = row
        key = url if url else (name.lower() if name else '')
        if key:
            if key in all_people:
                all_people[key]['email'] = email
                all_people[key]['phone'] = phone
                all_people[key]['classification'] = classification
            else:
                all_people[key] = {
                    'name': name or 'Accenture Contact',
                    'title': title or 'Professional',
                    'company': comp or 'Accenture',
                    'url': url or '',
                    'email': email or '',
                    'phone': phone or '',
                    'source': 'Career Intelligence Database',
                    'classification': classification or 'OTHER'
                }

# 3. From Recruiter_and_Hiring_Contacts_Master_Database.csv
rec_csv = os.path.join('data', 'Recruiter_and_Hiring_Contacts_Master_Database.csv')
if os.path.exists(rec_csv):
    with open(rec_csv, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for r in reader:
            row_str = " ".join(str(v) for v in r.values()).lower()
            if 'accenture' in row_str:
                name = r.get('Full Name') or r.get('Name') or r.get('name') or ''
                url = r.get('LinkedIn URL') or r.get('URL') or r.get('url') or ''
                title = r.get('Title') or r.get('Position') or r.get('Designation') or 'Recruiter'
                email = r.get('Email') or r.get('email') or ''
                phone = r.get('Phone') or r.get('phone') or ''
                key = url if url else name.lower()
                if key and key not in all_people:
                    all_people[key] = {
                        'name': name,
                        'title': title,
                        'company': 'Accenture',
                        'url': url,
                        'email': email,
                        'phone': phone,
                        'source': 'Recruiter Master Database',
                        'classification': 'RECRUITER'
                    }

print(f"Total Unique Accenture People Found Across All Databases: {len(all_people)}")

people_list = list(all_people.values())
with open('all_accenture_people_master.json', 'w', encoding='utf-8') as f:
    json.dump(people_list, f, indent=2)

# Count by category
categories = {
    'Recruiters & Talent Acquisition': [],
    'Procurement, SCM & Order Operations': [],
    'Consulting, Management & Strategy': [],
    'Software, Engineering & Cloud Tech': [],
    'HR Service Delivery & People Operations': [],
    'General Business Operations & Quality': []
}

for p in people_list:
    t = (p.get('title') or '').lower()
    if any(w in t for w in ['recruiter', 'recruiting', 'talent acquisition', 'talent fulfilment']) or p.get('is_recruiter') == '1' or p.get('classification') == 'RECRUITER':
        categories['Recruiters & Talent Acquisition'].append(p)
    elif any(w in t for w in ['procurement', 'sourcing', 'supply chain', 'order', 'p2p', 'purchasing']):
        categories['Procurement, SCM & Order Operations'].append(p)
    elif any(w in t for w in ['consulting', 'manager', 'lead', 'director', 'head', 'vp', 'architecture']):
        categories['Consulting, Management & Strategy'].append(p)
    elif any(w in t for w in ['software', 'engineer', 'developer', 'cloud', 'tech support', 'data engineering', 'infra']):
        categories['Software, Engineering & Cloud Tech'].append(p)
    elif any(w in t for w in ['hr', 'human resources', 'people advisor', 'workforce']):
        categories['HR Service Delivery & People Operations'].append(p)
    else:
        categories['General Business Operations & Quality'].append(p)

print("\n--- Distribution Across Functional Clusters ---")
for cat, lst in categories.items():
    print(f"  • {cat}: {len(lst)} people")

with open('all_accenture_people_categorized.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, indent=2)
