import urllib.request
import json

test_ids = [
    'AIOC-S01667752',
    'AIOC-S01667098',
    'AIOC-S01662040'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Search via CXS API
url = 'https://accenture.wd103.myworkdayjobs.com/wday/cxs/accenture/AccentureCareers/jobs'

for tid in test_ids:
    payload = json.dumps({'searchText': tid, 'limit': 5}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"Results for {tid}: {data.get('total', 0)}")
            for item in data.get('jobPostings', []):
                print(f"  -> {item.get('title')} | {item.get('externalPath')} | {item.get('postedOn')}")
    except Exception as e:
        print(f"Error for {tid}: {e}")
