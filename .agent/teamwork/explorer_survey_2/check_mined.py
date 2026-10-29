import json
import os

files = [
    'data/BANGALORE_LIVE_MINED_JOBS.json',
    'data/LIVE_ONLINE_SCRAPED_ROLES_2026.json',
    'data/TARGET_300_JOB_STRIKE.json',
    'data/BENGALURU_MASTER_JD_INTELLIGENCE.json',
    'data/BANGALORE_CURRENT_MONTH_JOBS.json'
]

target_companies = [
    'accenture', 'deloitte', 'goldman', 'amazon', 'ibm',
    'jpmorgan', 'jp morgan', 'kpmg', 'pwc',
    'walmart', 'delhivery', 'phonepe'
]

for p in files:
    if os.path.exists(p):
        print(f"=== {p} ===")
        try:
            with open(p, 'r', encoding='utf-8') as f:
                d = json.load(f)
            items = d if isinstance(d, list) else d.get('jobs', d.get('roles', []))
            print(f"Total items: {len(items)}")
            matched_count = 0
            for item in items:
                comp = str(item.get('company') or item.get('company_name', '')).lower()
                for tc in target_companies:
                    if tc in comp:
                        matched_count += 1
                        role = item.get('title') or item.get('role') or item.get('job_title')
                        jid = item.get('id') or item.get('job_id') or item.get('req_id')
                        loc = item.get('location')
                        link = item.get('url') or item.get('link') or item.get('career_url')
                        if matched_count <= 10:
                            print(f"  [{tc.upper()}] {jid} | {role} | {loc} | {link}")
                        break
            print(f"Total matched for targets: {matched_count}")
        except Exception as e:
            print("Error reading", p, e)
