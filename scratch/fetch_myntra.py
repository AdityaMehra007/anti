import urllib.request
import ssl
import json
import re

url = "https://jobs.myntra.com/home"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers=headers)
try:
    res = urllib.request.urlopen(req, context=ctx)
    print("STATUS:", res.status)
    print("FINAL URL:", res.geturl())
    html = res.read().decode("utf-8", errors="ignore")
    print("LENGTH:", len(html))
    with open("scratch/myntra_home.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved scratch/myntra_home.html")
except Exception as e:
    print("ERROR:", e)
