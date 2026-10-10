import re

with open("scratch/search_walmart_endpoints.py") as f:
    pass

import urllib.request
url = "https://i5.walmartimages.com/dfw/6019e67e-4d91/b4d18730-9880-4875-906b-0d9cb9d9c03b/v2/_next/static/chunks/3334-09214f5396fa65c2.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    code = resp.read().decode('utf-8')

# Search around hybrid-search
idx = code.find("hybrid-search")
if idx != -1:
    snippet = code[max(0, idx - 500): min(len(code), idx + 800)]
    print("Found hybrid-search snippet:")
    print(snippet)
else:
    print("hybrid-search not found")
