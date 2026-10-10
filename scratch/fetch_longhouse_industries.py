import urllib.request
import ssl
import gzip
from bs4 import BeautifulSoup
import re

url = "https://longhouse.in/industries-we-serve/"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip, deflate"})
res = urllib.request.urlopen(req, context=ctx)
html = gzip.decompress(res.read()).decode("utf-8", errors="ignore")
soup = BeautifulSoup(html, "html.parser")

print("Industries Page Title:", soup.title.string.strip() if soup.title else "")
for h in soup.find_all(["h2", "h3", "h4"]):
    t = h.get_text(strip=True).encode('ascii', errors='replace').decode()
    if t and len(t) < 50:
        print("  Industry / Focus:", t)
