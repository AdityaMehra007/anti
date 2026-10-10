import urllib.request
import ssl
import json
import re

url = "https://jobs.myntra.com/main.dart.js"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, context=ctx).read().decode("utf-8", errors="ignore")

for endpoint in ["/requisition/aggregation/_search?", "/requisition/_count", "/requisition/"]:
    idx = content.find(endpoint)
    if idx != -1:
        print(f"\n================= ENDPOINT: {endpoint} =================")
        print(content[idx-200:idx+800])
