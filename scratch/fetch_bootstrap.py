import urllib.request
import ssl
import re

url = "https://jobs.myntra.com/flutter_bootstrap.js"
ctx = ssl._create_unverified_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

req = urllib.request.Request(url, headers=headers)
content = urllib.request.urlopen(req, context=ctx).read().decode("utf-8", errors="ignore")
print("flutter_bootstrap.js length:", len(content))
with open("scratch/flutter_bootstrap.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Saved scratch/flutter_bootstrap.js")
