with open("scratch/search_spire.py", "r") as f:
    pass

import urllib.request
import ssl
import re

url = "https://jobs.myntra.com/main.dart.js"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, context=ctx).read().decode("utf-8", errors="ignore")

idx = content.find('r($,"dUD"')
print("Snippet around r($, \"dUD\"):")
print(content[idx-400:idx+400])
