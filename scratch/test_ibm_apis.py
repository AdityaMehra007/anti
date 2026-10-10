import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Test careers.ibm.com search API
urls = [
    "https://careers.ibm.com/api/jobs?location=Bengaluru&country=India&page=1",
    "https://careers.ibm.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=15&Distance=50&RadiusUnitType=0&Keywords=&Location=Bengaluru&ShowRadius=False&IsSearch=true",
    "https://ibm.eightfold.ai/api/apply/v2/jobs?domain=ibm.com&location=Bengaluru",
]

for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            print(f"URL {u[:50]}... Success, len: {len(content)}")
            print("Preview:", content[:200])
    except Exception as e:
        print(f"URL {u[:50]}... Failed: {e}")
