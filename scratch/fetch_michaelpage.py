import urllib.request
import ssl

url = "https://www.michaelpage.co.in/jobs/bangalore"
ctx = ssl._create_unverified_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}

req = urllib.request.Request(url, headers=headers)
try:
    res = urllib.request.urlopen(req, context=ctx)
    print("STATUS:", res.status)
    print("FINAL URL:", res.geturl())
    html = res.read().decode("utf-8", errors="ignore")
    print("LENGTH:", len(html))
    with open("scratch/michaelpage_bangalore.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved scratch/michaelpage_bangalore.html")
except Exception as e:
    print("ERROR:", e)
