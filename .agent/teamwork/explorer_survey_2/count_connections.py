import csv

target_companies = {
    'accenture': 'Accenture',
    'deloitte': 'Deloitte',
    'goldman': 'Goldman Sachs',
    'amazon': 'Amazon',
    'ibm': 'IBM',
    'jpmorgan': 'JPMorganChase',
    'jp morgan': 'JPMorganChase',
    'kpmg': 'KPMG',
    'pwc': 'PwC',
    'pricewaterhouse': 'PwC',
    'walmart': 'Walmart Global Tech',
    'delhivery': 'Delhivery',
    'phonepe': 'PhonePe'
}

company_counts = {v: {'total': 0, 'recruiters': 0, 'managers': 0, 'sample_titles': set()} for v in set(target_companies.values())}

# check Connections_clean.csv
with open('data/Connections_clean.csv', mode='r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    print("Fields in Connections_clean.csv:", reader.fieldnames)
    for r in reader:
        comp = str(r.get('Company') or r.get('company', '')).lower()
        matched = None
        for k, v in target_companies.items():
            if k in comp:
                matched = v
                break
        if matched:
            company_counts[matched]['total'] += 1
            pos = str(r.get('Position') or r.get('position', '')).lower()
            if any(w in pos for w in ['recruiter', 'talent', 'hr', 'ta ', 'human resources', 'staffing']):
                company_counts[matched]['recruiters'] += 1
            if any(w in pos for w in ['manager', 'lead', 'director', 'vp', 'head', 'vice president']):
                company_counts[matched]['managers'] += 1
            if len(company_counts[matched]['sample_titles']) < 5:
                company_counts[matched]['sample_titles'].add(r.get('Position') or r.get('position', ''))

print("\n=== LINKEDIN NETWORK DISTRIBUTION FOR 11 TARGETS ===")
for c, d in sorted(company_counts.items(), key=lambda x: x[1]['total'], reverse=True):
    print(f"{c:20} | Total Connections: {d['total']:3} | Recruiters/HR: {d['recruiters']:2} | Managers/Leads: {d['managers']:2}")
