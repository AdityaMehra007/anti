import urllib.request
import re

chunks = [
    "https://i5.walmartimages.com/dfw/6019e67e-4d91/b4d18730-9880-4875-906b-0d9cb9d9c03b/v2/_next/static/chunks/pages/_app-9edc24be502dfa1c.js",
    "https://i5.walmartimages.com/dfw/6019e67e-4d91/b4d18730-9880-4875-906b-0d9cb9d9c03b/v2/_next/static/chunks/main-f23a933feea9dc34.js"
]

for url in chunks:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        code = resp.read().decode('utf-8')
        print(f"File {url.split('/')[-1]}: {len(code)} bytes")
        if "careers/components/searchresults" in code:
            print("  Found searchresults component reference!")
            # let's see which chunk it imports
            pos = code.find("careers/components/searchresults")
            print(code[max(0, pos-200):min(len(code), pos+300)])
