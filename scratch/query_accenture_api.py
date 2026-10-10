import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
url = 'https://www.accenture.com/api/accenture/elastic/findjobs'

# Multipart form-data payload for Accenture Elastic Search
boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
lines = []

params = {
    'startIndex': '0',
    'maxResultSize': '24',
    'jobKeyword': '',
    'jobCountry': 'in',
    'jobLanguage': 'en',
    'countrySite': 'in-en',
    'sortBy': 'relevance',
    'searchType': 'vectorSearch',
    'enableQueryBoost': 'true',
    'totalHits': 'true',
    'jobFilters': json.dumps([
        {
            'fieldName': 'locations',
            'items': ['Bengaluru', 'Bangalore'],
            'multiSelect': False
        },
        {
            'fieldName': 'jobType',
            'items': ['Experience: 0-2 years'],
            'multiSelect': False
        }
    ])
}

body_parts = []
for k, v in params.items():
    body_parts.append(f'--{boundary}')
    body_parts.append(f'Content-Disposition: form-data; name="{k}"\r\n')
    body_parts.append(v)
body_parts.append(f'--{boundary}--\r\n')
body_bytes = '\r\n'.join(body_parts).encode('utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': f'multipart/form-data; boundary={boundary}',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://www.accenture.com',
    'Referer': 'https://www.accenture.com/in-en/careers/jobsearch?jt=Experience%3A%200-2%20years&et=Full-time'
}

print('Connecting to Accenture Elastic findjobs API...')
try:
    req = urllib.request.Request(url, data=body_bytes, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=25) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print('Status:', resp.status)
        print('Response keys:', list(data.keys()))
        total = data.get('totalHits', data.get('total', 0))
        print('Total hits:', total)
        jobs = data.get('results', data.get('jobs', []))
        print('Results count:', len(jobs))
        with open('scratch/accenture_elastic_jobs.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        if jobs:
            print('Sample job keys:', list(jobs[0].keys()))
            for j in jobs[:5]:
                print(f"[{j.get('jobId')}] {j.get('title')} | {j.get('locations')} | {j.get('postedDate')}")
except Exception as e:
    print('Error:', e)
