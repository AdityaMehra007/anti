import urllib.request
import ssl
import re

url = "https://jobs.myntra.com/main.dart.js"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, context=ctx).read().decode("utf-8", errors="ignore")

# Find `.X7=` or `X7(a){`
for m in re.finditer(r'X7\([a-zA-Z0-9_,]*\)\{', content):
    start = max(0, m.start() - 50)
    end = min(len(content), m.end() + 600)
    print("--- X7 METHOD DEFINITION ---")
    print(content[start:end])
