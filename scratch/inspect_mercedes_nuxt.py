import urllib.request
import re

url = 'https://jobs.mercedes-benz.com/_nuxt/CyRj1Orn.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        js = resp.read().decode('utf-8', errors='ignore')
        print(f"Nuxt entry loaded: {len(js)} bytes")
        with open('scratch/mercedes_nuxt.js', 'w', encoding='utf-8') as f:
            f.write(js)
        # Find paths with /api/ or gjb or search
        paths = set(re.findall(r'/[a-zA-Z0-9_\-\.\/]+', js))
        for p in paths:
            if any(k in p.lower() for k in ['job', 'search', 'filter', 'gjb', 'v1', 'v2', 'posting']):
                print("Path:", p)
except Exception as e:
    print(f"Error: {e}")
