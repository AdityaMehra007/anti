import urllib.request
import json
from datetime import datetime

url = 'https://accenture.wd103.myworkdayjobs.com/wday/cxs/accenture/AccentureCareers/jobs'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# We can query with location Bangalore/Bengaluru and sort or scan all pages
all_recent = []
limit = 20

# Let's search for Bengaluru jobs
for offset in range(0, 100, limit):
    payload = json.dumps({
        'appliedFacets': {
            'locationCountry': ['d430ebcb8f4f46a9926839bc4e460021'] # India
        },
        'searchText': 'Bengaluru New Associate',
        'limit': limit,
        'offset': offset
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            postings = data.get('jobPostings', [])
            if not postings:
                break
            for p in postings:
                posted = p.get('postedOn', '')
                title = p.get('title', '')
                path = p.get('externalPath', '')
                bullets = p.get('bulletFields', [])
                locationsText = p.get('locationsText', '')
                
                # Check if it contains Bengaluru
                if 'Bengaluru' in locationsText or 'Bengaluru' in path:
                    all_recent.append({
                        'title': title,
                        'posted': posted,
                        'path': path,
                        'locations': locationsText,
                        'link': f"https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers{path}"
                    })
    except Exception as e:
        print(f"Error at offset {offset}: {e}")
        break

print(f"Found {len(all_recent)} New Associate postings for Bengaluru.")
with open('latest_bengaluru_new_associates.json', 'w', encoding='utf-8') as f:
    json.dump(all_recent, f, indent=2)

# Print jobs posted recently: "Posted Today", "Posted Yesterday", "Posted 2 Days Ago", "Posted 3 Days Ago", etc.
print("\n--- Absolute Freshest Postings ---")
for x in all_recent:
    p = x['posted'].lower()
    if 'today' in p or 'yesterday' in p or 'day' in p and not '30+' in p:
        print(f"{x['title']} | {x['posted']} | {x['link']}")
