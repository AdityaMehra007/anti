import re

with open("scratch/walmart_page.html") as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
for s in scripts:
    if "_next/static/chunks" in s:
        try:
            import urllib.request
            req = urllib.request.Request(s, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
                if "searchresults" in content:
                    print(f"Match 'searchresults' in {s.split('/')[-1]}!")
                    # look for fetch, api, or endpoint
                    apis = set(re.findall(r'["\'](/api/[^"\']+)["\']', content))
                    if apis:
                        print("  APIs:", apis)
                    endpoints = set(re.findall(r'https?://[^\s"\'`<>]+', content))
                    valid = [e for e in endpoints if "walmart" in e or "api" in e or "job" in e]
                    if valid:
                        print("  Endpoints:", set(valid[:5]))
        except Exception as e:
            print("Error:", e)
