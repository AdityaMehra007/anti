import csv

pwc_contacts = []
with open(r'e:\anti\data\ALL_CONNECTIONS_OUTREACH_MASTER.csv', 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        comp = row.get('company', '') + ' ' + row.get('target_company', '')
        if 'pwc' in comp.lower():
            pwc_contacts.append(row)

print(f"Total PwC contacts in ALL_CONNECTIONS_OUTREACH_MASTER.csv: {len(pwc_contacts)}")
for i, c in enumerate(pwc_contacts[:10], 1):
    print(f"{i}. {c['full_name']} | {c['position']} | {c['company']} | target_comp={c['target_company']} | URL: {c['profile_url']}")
