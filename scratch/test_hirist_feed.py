import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

urls = [
    ('Product Jobs', 'https://www.hirist.tech/product-jobs?source=homepage'),
    ('E-commerce Jobs', 'https://www.hirist.tech/ecommerce-jobs?source=catlist'),
    ('FinTech & EdTech Jobs', 'https://www.hirist.tech/fintech-edtech-jobs?source=catlist')
]

for label, u in urls:
    try:
        html = urllib.request.urlopen(urllib.request.Request(u, headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
        if m:
            d = json.loads(m.group(1))
            jobfeed = d.get('props', {}).get('pageProps', {}).get('initialState', {}).get('job', {}).get('jobfeed', [])
            print(f"{label} -> jobfeed length: {len(jobfeed)}")
            if jobfeed:
                sample = jobfeed[0]
                print(f"   Sample keys: {list(sample.keys())}")
                print(f"   Sample title: {sample.get('title')}")
                print(f"   Sample company: {sample.get('cName') or sample.get('companyName')}")
                print(f"   Sample loc: {sample.get('locations') or sample.get('location')}")
                print(f"   Sample exp: {sample.get('minExp')} - {sample.get('maxExp')}")
                print(f"   Sample id: {sample.get('id') or sample.get('jobId')}")
                print(f"   Sample url: {sample.get('url') or sample.get('jobUrl')}")
    except Exception as e:
        print(f"Error {label}:", e)
