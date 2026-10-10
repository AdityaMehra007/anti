import urllib.request
import ssl
import json

ctx = ssl._create_unverified_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

files = [
    "assets/AssetManifest.json",
    "assets/AssetManifest.bin.json",
    "assets/FontManifest.json",
    "assets/assets/config.json",
    "assets/assets/env.json",
    "assets/assets/app_config.json"
]

for f in files:
    url = f"https://jobs.myntra.com/{f}"
    try:
        req = urllib.request.Request(url, headers=headers)
        res = urllib.request.urlopen(req, context=ctx)
        content = res.read().decode("utf-8", errors="ignore")
        print(f"[{f}] FOUND! Length: {len(content)}")
        if "Manifest" in f or "config" in f:
            print(content[:500])
            with open(f"scratch/{f.replace('/', '_')}", "w", encoding="utf-8") as out:
                out.write(content)
    except Exception as e:
        print(f"[{f}] {e}")
