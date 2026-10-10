import urllib.request
import ssl
import gzip
from bs4 import BeautifulSoup
import re

url = "https://www.abcconsultants.in/contact-us/"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip, deflate"})
res = urllib.request.urlopen(req, context=ctx)
html = gzip.decompress(res.read()).decode("utf-8", errors="ignore")
soup = BeautifulSoup(html, "html.parser")

print("Contact page title:", soup.title.string.encode('ascii', errors='replace').decode() if soup.title else "")

# Search for Bangalore office
for el in soup.find_all(string=re.compile(r'bangalore|bengaluru', re.I)):
    parent = el.parent
    block = parent.find_parent(["div", "li", "p", "section"])
    if block:
        text = block.get_text("\n", strip=True)
        print("--- BANGALORE OFFICE BLOCK ---")
        print(text.encode('ascii', errors='replace').decode())
        print()
        break
