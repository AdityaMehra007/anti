import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://flipkart.turbohire.co/main.66fd13673f8a0eb06cf0.chunk.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as resp:
    js = resp.read().decode('utf-8', errors='ignore')

# find occurrences of isMatched in js
matches = re.findall(r'.{0,50}isMatched.{0,50}', js)
print(f"Found {len(matches)} occurrences of isMatched:")
for m in matches[:5]:
    print(" ", m.strip())
