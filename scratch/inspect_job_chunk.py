import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.phonepe.com/webstatic/15170/component---src-pages-careers-job-openings-index-js-1f7467adb370882a0aba.js"
headers = {'User-Agent': 'Mozilla/5.0'}
with urllib.request.urlopen(urllib.request.Request(url, headers=headers), context=ctx) as resp:
    js = resp.read().decode('utf-8', errors='ignore')

print(f"Job openings chunk len: {len(js)}")

# find api urls or endpoints
apis = re.findall(r'https?://[^\s"\'`]+', js)
print("APIs in job openings chunk:")
for a in set(apis):
    print(" ", a)

# check for greenhouse board token or api calls
gh = re.findall(r'["\']([a-zA-Z0-9_/.-]*(?:greenhouse|lever|darwinbox|jobs|departments|career)[a-zA-Z0-9_/.-]*)["\']', js)
print("Endpoints/tokens found:")
for g in set(gh):
    if len(g) > 4:
        print(" ", g)
