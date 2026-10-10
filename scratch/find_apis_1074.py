import urllib.request
import re

url = "https://i5.walmartimages.com/dfw/6019e67e-4d91/b4d18730-9880-4875-906b-0d9cb9d9c03b/v2/_next/static/chunks/1074-023ca96731e8c075.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    code = resp.read().decode('utf-8')

print("Chunk 1074 length:", len(code))
# find all /api/ or endpoints or URLs
apis = set(re.findall(r'["\'](/api/[^"\']+)["\']', code))
print("APIs in chunk 1074:")
for a in apis:
    print(" ", a)

urls = set(re.findall(r'https?://[^\s"\'`<>]+walmart[^\s"\'`<>]*', code))
print("Walmart URLs in 1074:")
for u in urls:
    print(" ", u)
