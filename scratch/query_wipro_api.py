import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
url = 'https://careers.wipro.com/services/recruiting/v1/jobs'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://careers.wipro.com',
    'Referer': 'https://careers.wipro.com/search/?locationsearch=Bengaluru'
}

payload = {
    'keywords': '',
    'locale': 'en_US',
    'location': 'Bengaluru',
    'pageNumber': 1,
    'sortBy': 'recent'
}

print('Querying Wipro SuccessFactors endpoint...')
try:
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print('Status:', resp.status)
        total = data.get('totalJobs')
        jobs = data.get('jobSearchResult', [])
        print(f'Total jobs in Bengaluru at Wipro: {total}')
        print(f'Fetched on page 1: {len(jobs)}')
        with open('scratch/wipro_blr_jobs.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        for j in jobs[:8]:
            r = j.get('response', {})
            jid = r.get('id')
            title = r.get('unifiedStandardTitle')
            loc = r.get('jobLocation')
            posted = r.get('postedDate')
            print(f"- [{jid}] {title} | {loc} | {posted}")
except Exception as e:
    print('Error:', e)
