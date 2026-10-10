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

for card in soup.find_all(class_=re.compile(r'team|leader|member|col', re.I)):
    h_tag = card.find(["h2", "h3", "h4"])
    if h_tag and any(m in card.prettify() for m in ["@abcconsultants.in", "Director", "President", "Managing"]):
        name = h_tag.get_text(strip=True)
        sub = card.find(class_=re.compile(r'designation|title|role|sub', re.I))
        role = sub.get_text(strip=True) if sub else ""
        mailto = card.find("a", href=re.compile(r'mailto:'))
        email = mailto["href"].replace("mailto:", "").strip() if mailto else ""
        if name and email:
            print(f"Name: {name} | Role: {role} | Email: {email}")
