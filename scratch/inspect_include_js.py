import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.flipkartcareers.com/includes/include.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        print(f"include.js len: {len(content)}")
        # print api or urls
        urls = re.findall(r'https?://[^\s"\'`]+', content)
        print("URLs in include.js:", set(urls))
        # check turbohire or job apis
        apis = re.findall(r'[\'"]([^\'"]*(?:api|job|turbohire)[^\'"]*)[\'"]', content)
        print("Endpoints in include.js:", set(apis))
except Exception as e:
    print(f"Error: {e}")
