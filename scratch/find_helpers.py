import urllib.request
import ssl
import re

url = "https://jobs.myntra.com/main.dart.js"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, context=ctx).read().decode("utf-8", errors="ignore")

# Find occurrences of r($,
matches = list(re.finditer(r'r\(\$,', content))
print(f"Total r($, calls: {len(matches)}")

for m in matches:
    snippet = content[m.start():m.start()+80]
    if any(k in snippet for k in ['"T7"', '"ex"', '"aP"', '"c1"', '"ap"', '"bj"']):
        print(snippet)
