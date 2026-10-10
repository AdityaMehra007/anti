import urllib.request
import ssl
import re

files_to_check = [
    "flutter_bootstrap.js",
    "main.dart.js",
    "flutter.js"
]

ctx = ssl._create_unverified_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for fname in files_to_check:
    url = f"https://jobs.myntra.com/{fname}"
    try:
        req = urllib.request.Request(url, headers=headers)
        res = urllib.request.urlopen(req, context=ctx)
        print(f"[{fname}] STATUS: {res.status}, SIZE: {len(res.read())}")
    except Exception as e:
        print(f"[{fname}] ERROR: {e}")
