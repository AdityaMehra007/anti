import urllib.request
import ssl
import re

url = "https://jobs.myntra.com/main.dart.js"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, context=ctx).read().decode("utf-8", errors="ignore")

# Find occurrences of dUD and dUC
for target in ['"dUD"', '"dUC"']:
    for m in re.finditer(re.escape(target), content):
        print(f"--- MATCH {target} ---")
        start = max(0, m.start() - 50)
        end = min(len(content), m.end() + 200)
        print(content[start:end])

# Find usages of $.i6() or $.IY() or dUD or dUC
for target in ['$.i6()', '$.IY()', 'dUD', 'dUC']:
    matches = list(re.finditer(re.escape(target), content))
    print(f"Target {target}: {len(matches)} matches")
    for m in matches[:5]:
        start = max(0, m.start() - 100)
        end = min(len(content), m.end() + 150)
        print(f"Context for {target}:", content[start:end])
