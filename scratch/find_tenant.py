with open("scratch/search_spire.py", "r") as f:
    pass

import urllib.request
import ssl
import re

with open("scratch/myntra_home.html", "r") as f:
    pass

url = "https://jobs.myntra.com/main.dart.js"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, context=ctx).read().decode("utf-8", errors="ignore")

idx = content.find("https://io.spire2grow.com/ies/")
if idx != -1:
    print("Found prod URL! Context:")
    print(content[idx-200:idx+800])

idx_anI = content.find("anI")
matches_anI = [m.start() for m in re.finditer(r'anI', content)]
print(f"anI occurrences: {len(matches_anI)}")
for m in matches_anI[:10]:
    print("Context around anI:", content[m-50:m+150])
