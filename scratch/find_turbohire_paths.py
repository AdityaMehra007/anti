import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://flipkart.turbohire.co/18.dbc8e48216e40dca22f4.chunk.js"
headers = {'User-Agent': 'Mozilla/5.0'}
with urllib.request.urlopen(urllib.request.Request(url, headers=headers), context=ctx) as resp:
    js = resp.read().decode('utf-8', errors='ignore')

# look for careerpage or job search paths
paths = re.findall(r'["\'](/api/[^"\']+)["\']', js)
print("Paths in chunk 18:")
for p in set(paths):
    if any(k in p.lower() for k in ["job", "career", "public", "candidate", "dashboard"]):
        print(" ", p)
