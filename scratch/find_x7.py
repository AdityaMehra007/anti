import urllib.request
import ssl
import re

url = "https://jobs.myntra.com/main.dart.js"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, context=ctx).read().decode("utf-8", errors="ignore")

# In the previous snippet:
# l = n.X7(a)
# if (J.bd(l) !== 0) m = J.LR(m, l)
# Let's find definition of X7
matches = list(re.finditer(r'X7\(', content))
print("Occurrences of X7(:", len(matches))
for m in matches[:5]:
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 250)
    print("--- MATCH ---")
    print(content[start:end])
