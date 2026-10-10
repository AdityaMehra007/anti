import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
url = 'https://careers.wipro.com/services/recruiting/v1/jobs'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Content-Type': 'application/json',
    'Origin': 'https://careers.wipro.com',
    'Referer': 'https://careers.wipro.com/search/?locationsearch=Bengaluru'
}

queries = ['Analyst', 'Associate', 'Operations', 'Finance', 'Procurement', 'HR', 'Supply Chain']
for q in queries:
    payload = {'keywords': q, 'locale': 'en_US', 'location': 'Bengaluru', 'pageNumber': 1, 'sortBy': 'recent'}
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        total = data.get('totalJobs')
        jobs = data.get('jobSearchResult', [])
        print(f"Query [{q}] -> Total in Bengaluru: {total}")
        for j in jobs[:4]:
            r = j.get('response', {})
            jid = r.get('id')
            title = r.get('unifiedStandardTitle')
            url_title = r.get('urlTitle')
            link = f"https://careers.wipro.com/job/Bengaluru/{url_title}/{jid}-en_US" if url_title else f"https://careers.wipro.com/job/{jid}"
            print(f"   [{jid}] {title} -> {link}")
