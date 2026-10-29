import json
import csv
import os

target_names = {
    'accenture': 'Accenture',
    'deloitte': 'Deloitte',
    'goldman': 'Goldman Sachs',
    'amazon': 'Amazon',
    'ibm': 'IBM',
    'jpmorgan': 'JPMorganChase',
    'kpmg': 'KPMG',
    'pwc': 'PwC',
    'walmart': 'Walmart Global Tech',
    'delhivery': 'Delhivery',
    'phonepe': 'PhonePe'
}

def match_target(comp):
    c = str(comp).lower()
    for k, v in target_names.items():
        if k in c:
            return v
    return None

results = []

# 1. BBA_IB_Bengaluru_61_Job_Pipeline.csv
with open('data/BBA_IB_Bengaluru_61_Job_Pipeline.csv', mode='r', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        matched = match_target(r['Company Name'])
        if matched:
            results.append({
                'source': 'BBA_IB_Bengaluru_61_Job_Pipeline.csv',
                'target_company': matched,
                'company_raw': r['Company Name'],
                'role': r['Job Title'],
                'job_id': r['Job ID'],
                'fit_score': r['Fit Score'],
                'url': r['Direct Requisition Link'],
                'location': r['Location']
            })

# 2. Check 61_job_complete_referral_audit.csv
with open('data/61_job_complete_referral_audit.csv', mode='r', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        matched = match_target(r['Target Company'])
        if matched:
            # check if we already have it or can enrich it
            pass

# 3. Check BANGALORE_SCORED_JOBS_MASTER.json
if os.path.exists('data/BANGALORE_SCORED_JOBS_MASTER.json'):
    try:
        with open('data/BANGALORE_SCORED_JOBS_MASTER.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            items = data if isinstance(data, list) else data.get('jobs', [])
            for item in items:
                comp = item.get('company') or item.get('company_name', '')
                matched = match_target(comp)
                if matched:
                    results.append({
                        'source': 'BANGALORE_SCORED_JOBS_MASTER.json',
                        'target_company': matched,
                        'company_raw': comp,
                        'role': item.get('title') or item.get('job_title', ''),
                        'job_id': item.get('job_id') or item.get('id', ''),
                        'fit_score': item.get('score') or item.get('fit_score', ''),
                        'url': item.get('url') or item.get('link', ''),
                        'location': item.get('location', '')
                    })
    except Exception as e:
        print('Error BANGALORE_SCORED_JOBS_MASTER:', e)

# 4. Check BANGALORE_LIVE_MINED_JOBS.json
if os.path.exists('data/BANGALORE_LIVE_MINED_JOBS.json'):
    try:
        with open('data/BANGALORE_LIVE_MINED_JOBS.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            items = data if isinstance(data, list) else data.get('jobs', [])
            for item in items:
                comp = item.get('company') or item.get('company_name', '')
                matched = match_target(comp)
                if matched:
                    results.append({
                        'source': 'BANGALORE_LIVE_MINED_JOBS.json',
                        'target_company': matched,
                        'company_raw': comp,
                        'role': item.get('title') or item.get('job_title', ''),
                        'job_id': item.get('job_id') or item.get('id', ''),
                        'fit_score': item.get('score', ''),
                        'url': item.get('url') or item.get('link', ''),
                        'location': item.get('location', '')
                    })
    except Exception as e:
        print('Error BANGALORE_LIVE_MINED_JOBS:', e)

# 5. Check universal_dissected_jobs_500.json
with open('data/universal_dissected_jobs_500.json', 'r', encoding='utf-8') as f:
    dissected = json.load(f)['jobs']
    for item in dissected:
        comp = item.get('company', '')
        matched = match_target(comp)
        if matched:
            results.append({
                'source': 'universal_dissected_jobs_500.json',
                'target_company': matched,
                'company_raw': comp,
                'role': item.get('title', ''),
                'job_id': item.get('id', ''),
                'fit_score': item.get('ats_score', ''),
                'url': item.get('url', ''),
                'location': item.get('location', '')
            })

# 6. Check approval_queue.csv
if os.path.exists('data/approval_queue.csv'):
    with open('data/approval_queue.csv', mode='r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for r in reader:
            comp = r.get('company') or r.get('target_company') or r.get('Company', '')
            matched = match_target(comp)
            if matched:
                results.append({
                    'source': 'approval_queue.csv',
                    'target_company': matched,
                    'company_raw': comp,
                    'role': r.get('title') or r.get('role') or r.get('Job Title', ''),
                    'job_id': r.get('job_id') or r.get('req_id') or r.get('Docket ID') or r.get('docket_id', ''),
                    'fit_score': r.get('score') or r.get('ats_score') or r.get('Fit Score', ''),
                    'url': r.get('url') or r.get('link') or r.get('career_url', ''),
                    'location': r.get('location', '')
                })

print(f"Total matched items across sources: {len(results)}")
by_company = {}
for r in results:
    c = r['target_company']
    by_company.setdefault(c, []).append(r)

for c in sorted(target_names.values()):
    items = by_company.get(c, [])
    print(f"\n=== {c} ({len(items)} records) ===")
    seen = set()
    for item in items:
        sig = (item['role'], item['source'])
        if sig not in seen:
            seen.add(sig)
            print(f"  [{item['source']}] {item['job_id']} | {item['role']} | score: {item['fit_score']} | url: {item['url']} | loc: {item['location']}")
