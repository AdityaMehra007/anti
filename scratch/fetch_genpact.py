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

# Payload 1: Search for Bangalore / Bengaluru
payload = {
    'appliedFacets': {},
    'limit': 20,
    'offset': 0,
    'searchText': 'Bengaluru'
}

print('Connecting to Genpact Workday API...')
try:
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        total = data.get('total')
        job_postings = data.get('jobPostings', [])
        facets = data.get('facets', [])
        print(f'Total jobs matching Bengaluru: {total}')
        print(f'Fetched job postings: {len(job_postings)}')
        with open('scratch/genpact_blr.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        for j in job_postings:
            title = j.get('title')
            loc = j.get('locationsText')
            posted = j.get('postedOn')
            uri = j.get('externalPath')
            print(f"- {title} | {loc} | {posted} | {uri}")
except Exception as e:
    print('Error:', e)
