import urllib.request
import ssl
import gzip

url = "https://wellfound.com/jobs"
ctx = ssl._create_unverified_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate"
}

req = urllib.request.Request(url, headers=headers)
try:
    res = urllib.request.urlopen(req, context=ctx)
    print("STATUS:", res.status)
    print("FINAL URL:", res.geturl())
    content = res.read()
    if res.headers.get("Content-Encoding") == "gzip":
        html = gzip.decompress(content).decode("utf-8", errors="ignore")
    else:
        html = content.decode("utf-8", errors="ignore")
    print("LENGTH:", len(html))
    with open("scratch/wellfound_jobs.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved scratch/wellfound_jobs.html")
except urllib.error.HTTPError as e:
    print(f"HTTP ERROR {e.code}: {e.headers.get('Server', '')}")
except Exception as e:
    print("ERROR:", e)
