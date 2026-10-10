import urllib.request
import ssl

ctx = ssl._create_unverified_context()
headers = {"User-Agent": "Mozilla/5.0"}

scripts = [
    "job-search-banner-api.js",
    "jobs-landing-api.js",
    "module-dynamic-job-accord.js",
    "job-feed-card.js"
]

for s in scripts:
    url = f"https://www.diageo.com/en/javascripts/shared/{s}"
    try:
        req = urllib.request.Request(url, headers=headers)
        res = urllib.request.urlopen(req, context=ctx)
        content = res.read().decode("utf-8", errors="ignore")
        print(f"[{s}] STATUS: {res.status}, LEN: {len(content)}")
        with open(f"scratch/{s}", "w", encoding="utf-8") as out:
            out.write(content)
    except Exception as e:
        print(f"[{s}] ERROR: {e}")
