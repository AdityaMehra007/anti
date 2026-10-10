import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.ibm.com/in-en/careers/search?field_keyword_18%5B0%5D=Entry%20Level&source=WEB_ENTRY_INDIA"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# find all scripts
scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
for s in scripts:
    print("Script src:", s)

# check config or json inside HTML
script_contents = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
for sc in script_contents:
    if "api" in sc.lower() or "endpoint" in sc.lower() or "search" in sc.lower():
        lines = [line.strip() for line in sc.split('\n') if any(w in line.lower() for w in ["api", "endpoint", "url", "service", "query", "host"])]
        if lines:
            print("Found interesting lines in inline script:")
            for l in lines[:10]:
                print("  ", l[:120])
