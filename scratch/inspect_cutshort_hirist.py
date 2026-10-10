import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Cutshort inspect
try:
    html = urllib.request.urlopen(urllib.request.Request('https://cutshort.io/jobs/startup-jobs-in-bangalore-bengaluru', headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    if m:
        d = json.loads(m.group(1))
        queries = d.get('props', {}).get('pageProps', {}).get('dehydratedState', {}).get('queries', [])
        print(f"Cutshort queries: {len(queries)}")
        for q in queries:
            data = q.get('state', {}).get('data', {})
            if isinstance(data, dict):
                print("Cutshort data keys:", list(data.keys()))
                jobs = data.get('jobs', []) or data.get('data', []) or data.get('results', [])
                print(f"Cutshort jobs found: {len(jobs)}")
                if jobs:
                    print("Sample Cutshort job:", list(jobs[0].keys()) if isinstance(jobs[0], dict) else jobs[0])
except Exception as e:
    print("Cutshort inspect error:", e)

# Hirist inspect
try:
    html = urllib.request.urlopen(urllib.request.Request('https://www.hirist.tech/product-jobs?source=homepage', headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    if m:
        d = json.loads(m.group(1))
        initialState = d.get('props', {}).get('pageProps', {}).get('initialState', {})
        print("Hirist initialState keys:", list(initialState.keys()) if isinstance(initialState, dict) else type(initialState))
        if isinstance(initialState, dict):
            job_data = initialState.get('jobs', {}) or initialState.get('search', {})
            print("Hirist job_data keys:", list(job_data.keys()) if isinstance(job_data, dict) else type(job_data))
except Exception as e:
    print("Hirist inspect error:", e)
