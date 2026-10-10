import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.flipkartcareers.com/#!/joblist"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# look for scripts
scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
print("Scripts on flipkartcareers.com:")
for s in scripts:
    print(" ", s)

# look for angular or api calls
calls = re.findall(r'https?://[^\s"\'<>]+', html)
for c in set(calls):
    if "api" in c.lower() or "job" in c.lower():
        print("API:", c)
