import re

with open("scratch/parse_ibm.py") as f:
    pass

import urllib.request
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.ibm.com/in-en/careers/search?field_keyword_18%5B0%5D=Entry%20Level&source=WEB_ENTRY_INDIA"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# look for careerSearch or api endpoints in the html
vars_found = re.findall(r'careerSearch\w*\s*=\s*["\']([^"\']+)["\']', html)
print("careerSearch vars:", vars_found)

# look for any mention of api url or search host
hosts = re.findall(r'https?://[a-zA-Z0-9.-]+\.ibm\.com/[^\s"\'<>]*', html)
print("IBM urls found:")
for h in set(hosts):
    if any(k in h.lower() for k in ["job", "career", "search", "api"]):
        print(" ", h)
