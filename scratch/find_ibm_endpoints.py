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

# find endpoint in html
endpoints = re.findall(r'https?://[^\s"\'<>]+(?:api|search|jobs|brassring)[^\s"\'<>]*', html)
for ep in set(endpoints):
    print("Endpoint:", ep)
