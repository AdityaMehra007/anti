import urllib.request
import re

chunks = [
    "https://i5.walmartimages.com/dfw/6019e67e-4d91/b4d18730-9880-4875-906b-0d9cb9d9c03b/v2/_next/static/chunks/3334-09214f5396fa65c2.js",
    "https://i5.walmartimages.com/dfw/6019e67e-4d91/b4d18730-9880-4875-906b-0d9cb9d9c03b/v2/_next/static/chunks/1074-023ca96731e8c075.js",
    "https://i5.walmartimages.com/dfw/6019e67e-4d91/b4d18730-9880-4875-906b-0d9cb9d9c03b/v2/_next/static/chunks/b857c259-b34b2045e6b00cb9.js"
]

for url in chunks:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            print(f"Chunk {url.split('/')[-1]}: {len(content)} bytes")
            # find api or search or graphql or workday
            matches = re.findall(r'https?://[^\s"\'`<>]+', content)
            api_matches = [m for m in matches if any(k in m for k in ["api", "search", "graphql", "walmart", "workday", "job"])]
            if api_matches:
                print("  Matches:", set(api_matches[:10]))
            paths = re.findall(r'["\'](/api/[^"\'`\s]+)["\']', content)
            if paths:
                print("  API paths:", set(paths[:10]))
    except Exception as e:
        print(f"Error for {url}: {e}")
