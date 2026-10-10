import urllib.request
import ssl
import gzip
from bs4 import BeautifulSoup
import re

url = "https://www.abcconsultants.in/our-leadership-team/"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip, deflate"})
res = urllib.request.urlopen(req, context=ctx)
html = gzip.decompress(res.read()).decode("utf-8", errors="ignore")
soup = BeautifulSoup(html, "html.parser")

# Find all mailto links and their container text
for a in soup.find_all("a", href=re.compile(r'mailto:')):
    email = a["href"].replace("mailto:", "").strip()
    parent = a.find_parent(["div", "section", "article"])
    # get text up to 300 chars
    text = parent.get_text(" ", strip=True)[:250] if parent else ""
    # sanitize text for windows console
    text = text.encode('ascii', errors='replace').decode()
    print(f"Email: {email}")
    print(f"  Snippet: {text}\n")
