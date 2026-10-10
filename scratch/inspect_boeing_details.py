import json
import re

with open('scratch/boeing_detailed_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

for i, j in enumerate(jobs, 1):
    title = j['title']
    req = j.get('req_id', '')
    loc = j.get('loc', '')
    desc = j.get('description', '')
    
    print(f"=== {i}. [{req}] {title} | Loc: {loc} ===")
    lines = [l.strip() for l in desc.splitlines() if l.strip()]
    
    # print first 10 lines
    for l in lines[:10]:
        print("  ", l)
    
    # look for qualifications / degree / experience
    print("  --- Highlights ---")
    for l in lines:
        if any(k in l.lower() for k in ['qualification', 'bachelor', 'degree', 'experience', 'level', 'years', 'fresh', 'graduate', 'business']):
            print("   *", l[:120])
    print()
