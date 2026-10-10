import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.phonepe.com/webstatic/15170/app-c0e482ed312eda85e2f3.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as resp:
    js = resp.read().decode('utf-8', errors='ignore')

# look for api urls
apis = re.findall(r'https?://[^\s"\'`]+(?:api|job|career|greenhouse|darwinbox)[^\s"\'`]*', js)
print("APIs in app.js:", set(apis))

# look for relative api paths
paths = re.findall(r'["\'](/api/[^"\']+)["\']', js)
print("API paths in app.js:", set(paths))
