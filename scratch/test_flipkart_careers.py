import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.flipkartcareers.com/#!/joblist"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"flipkartcareers.com len: {len(html)}")
        # check for api or angular/react endpoints
        apis = re.findall(r'https?://[^\s"\'<>]+(?:api|job|career)[^\s"\'<>]*', html)
        print("APIs found:", set(apis[:10]))
except Exception as e:
    print(f"Error flipkartcareers: {e}")
