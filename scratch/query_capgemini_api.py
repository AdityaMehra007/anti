import urllib.request
import json
import ssl

ctx = ssl.create_default_context()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://www.capgemini.com',
    'Referer': 'https://www.capgemini.com/in-en/careers/'
}

# 1. Fetch available filters
filters_url = 'https://cg-jobstream-api.azurewebsites.net/api/job-filters/?country_code=in-en'
print('Fetching Capgemini India filters...')
try:
    req = urllib.request.Request(filters_url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
        filters_data = json.loads(resp.read().decode('utf-8'))
        with open('scratch/capgemini_filters.json', 'w', encoding='utf-8') as f:
            json.dump(filters_data, f, indent=2)
        print('Saved scratch/capgemini_filters.json')
except Exception as e:
    print('Filter fetch error:', e)

# 2. Fetch jobs
jobs_url = 'https://cg-jobstream-api.azurewebsites.net/api/job-search?country_code=in-en&page=1&size=20'
print('\nFetching Capgemini India jobs...')
try:
    req = urllib.request.Request(jobs_url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
        jobs_data = json.loads(resp.read().decode('utf-8'))
        with open('scratch/capgemini_jobs.json', 'w', encoding='utf-8') as f:
            json.dump(jobs_data, f, indent=2)
        print('Total jobs in India:', jobs_data.get('total'))
        print('Jobs on page 1:', len(jobs_data.get('jobs', [])))
except Exception as e:
    print('Jobs fetch error:', e)
