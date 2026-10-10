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

# find all axios / fetch urls or strings containing career or job
matches = re.findall(r'["\']([a-zA-Z0-9_/.-]*(?:careerpage|joblist|jobs|candidate|orgId)[a-zA-Z0-9_/.-]*)["\']', js)
print("Matches found:", len(matches))
for m in set(matches):
    if len(m) > 4 and not m.endswith('.js') and not m.endswith('.png'):
        print(" ", m)
