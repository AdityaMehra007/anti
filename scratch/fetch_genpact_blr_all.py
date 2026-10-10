import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
url = 'https://genpact.wd108.myworkdayjobs.com/wday/cxs/genpact/External_Careers/jobs'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

blr_loc_ids = [
    "faddece16d451000bf3f6b6fd3460000", # Surya Park, STPI, Bangalore (23)
    "faddece16d451000bf39602074150000", # Pritech Park Tower-5 (2)
    "faddece16d451000bf32840a7aae0000", # Pritech Park GF/11 (18)
    "faddece16d451000bf335d4335830000", # Pritech Park SEZ (1)
    "faddece16d451000bf4036b599930000", # Pritech Park SEZ-II (10)
    "faddece16d451000bf3d37688ca50000", # Prestige Technology Park IV, Bangalore (178)
    "faddece16d451000bf382b1b6ada0000", # Prestige Technology Park IV, GERC (12)
    "faddece16d451000bc25895401c30000"  # Bengaluru JP (1)
]

all_jobs = []
limit = 20

for offset in range(0, 260, limit):
    payload = {
        'appliedFacets': {
            'locations': blr_loc_ids
        },
        'limit': limit,
        'offset': offset,
        'searchText': ''
    }
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=25) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            total = data.get('total')
            postings = data.get('jobPostings', [])
            all_jobs.extend(postings)
            print(f'Offset {offset}: fetched {len(postings)} (Total: {total})')
            if not postings or len(all_jobs) >= total:
                break
    except Exception as e:
        print(f'Error at offset {offset}:', e)
        break

print(f'Total Bangalore jobs fetched: {len(all_jobs)}')
with open('scratch/genpact_all_bangalore_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(all_jobs, f, indent=2)
