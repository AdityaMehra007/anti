import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://careers.swiggy.in/assets/index-CbfQuJ9d.js"
headers = {'User-Agent': 'Mozilla/5.0'}

with urllib.request.urlopen(urllib.request.Request(url, headers=headers), context=ctx) as resp:
    js = resp.read().decode('utf-8', errors='ignore')

print(f"Swiggy index JS length: {len(js)}")

# find all api urls or backend endpoints
apis = re.findall(r'https?://[^\s"\'`]+', js)
print("APIs in bundle:")
for a in set(apis):
    if any(k in a.lower() for k in ["api", "job", "career", "swiggy"]):
        print(" ", a)

# find relative api paths
paths = re.findall(r'["\'](/api/[^"\']+|/jobs/[^"\']+|/career/[^"\']+)["\']', js)
print("Relative paths:")
for p in set(paths):
    print(" ", p)
