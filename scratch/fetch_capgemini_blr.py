import urllib.request
import json
import ssl
import time

ctx = ssl.create_default_context()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://www.capgemini.com',
    'Referer': 'https://www.capgemini.com/in-en/careers/'
}

all_bangalore_jobs = []
size = 50
total_bangalore = 235

for page in range(1, 6):
    url = f'https://cg-jobstream-api.azurewebsites.net/api/job-search?country_code=in-en&location=Bangalore&page={page}&size={size}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=25) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            jobs = data.get('data', [])
            all_bangalore_jobs.extend(jobs)
            print(f'Page {page}: fetched {len(jobs)} jobs (Cumulative: {len(all_bangalore_jobs)})')
            if not jobs or len(all_bangalore_jobs) >= data.get('total', 0):
                break
        time.sleep(0.2)
    except Exception as e:
        print(f'Error on page {page}:', e)
        break

print(f'\nTotal Capgemini Bangalore jobs fetched: {len(all_bangalore_jobs)}')
with open('scratch/capgemini_bangalore_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(all_bangalore_jobs, f, indent=2)
