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

# Empty payload to fetch total jobs and all facets
payload = {
    'appliedFacets': {},
    'limit': 1,
    'offset': 0,
    'searchText': ''
}

print('Fetching global facets from Genpact Workday...')
try:
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=25) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        total = data.get('total')
        print(f'Total global open jobs at Genpact: {total}')
        facets = data.get('facets', [])
        with open('scratch/genpact_global_facets.json', 'w', encoding='utf-8') as f:
            json.dump(facets, f, indent=2)
        print('Saved scratch/genpact_global_facets.json')
except Exception as e:
    print('Error:', e)
