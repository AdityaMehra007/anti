import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://flipkart.turbohire.co/30.83fbae2815ce51b795d9.chunk.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as resp:
    js = resp.read().decode('utf-8', errors='ignore')

# find endpoint paths in chunk 30
endpoints = re.findall(r'["\'](/api/[^"\']+)["\']', js)
print("Endpoints in chunk 30:")
for ep in set(endpoints):
    print(" ", ep)
