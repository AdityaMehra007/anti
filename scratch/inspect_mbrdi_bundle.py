import urllib.request
import re

url = 'https://www.mbrdi.co.in/static/js/main.37de2488.js'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
})
try:
    with urllib.request.urlopen(req) as resp:
        js = resp.read().decode('utf-8', errors='ignore')
        print(f"JS loaded, length: {len(js)}")
        with open('scratch/mbrdi_bundle.js', 'w', encoding='utf-8') as f:
            f.write(js)
        # Search for URLs
        urls = set(re.findall(r'https?://[^\s\"\'<>]+', js))
        print(f"Found URLs: {len(urls)}")
        for u in sorted(urls):
            if any(k in u.lower() for k in ['career', 'job', 'mercedes', 'daimler', 'talent', 'api', 'workday', 'successfactors', 'taleo', 'phenom']):
                print(f"  -> {u}")
except Exception as e:
    print(f"Error: {e}")
