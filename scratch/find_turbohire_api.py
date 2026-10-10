import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://flipkart.turbohire.co/main.66fd13673f8a0eb06cf0.chunk.js"
headers = {'User-Agent': 'Mozilla/5.0'}
with urllib.request.urlopen(urllib.request.Request(url, headers=headers), context=ctx) as resp:
    js = resp.read().decode('utf-8', errors='ignore')

# look for api urls in the js
api_urls = re.findall(r'https?://[a-zA-Z0-9.-]+\.turbohire\.co[^\s"\'`]*', js)
print("TurboHire URLs:", set(api_urls))

# look for path patterns with orgId or job
paths = re.findall(r'["\'](/api/[^"\']+|/career/[^"\']+|/jobs/[^"\']+)["\']', js)
print("API Paths:", set(paths[:15]))
