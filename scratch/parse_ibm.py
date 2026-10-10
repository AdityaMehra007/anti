import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.ibm.com/in-en/careers/search?field_keyword_18%5B0%5D=Entry%20Level&source=WEB_ENTRY_INDIA"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req, context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

m = re.search(r'id=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>', html, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    print("Found NEXT_DATA keys:", list(data.keys()))
    with open("scratch/ibm_next_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Saved ibm_next_data.json")
    
    # check if jobs or search config is in pageProps
    props = data.get("props", {})
    pageProps = props.get("pageProps", {})
    print("pageProps keys/type:", type(pageProps), len(pageProps) if isinstance(pageProps, (list, dict)) else pageProps)
else:
    print("No __NEXT_DATA__ match")
