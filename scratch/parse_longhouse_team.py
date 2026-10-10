import urllib.request
import ssl
import gzip
from bs4 import BeautifulSoup
import re

url = "https://longhouse.in/about-us/"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip, deflate"})
res = urllib.request.urlopen(req, context=ctx)
html = gzip.decompress(res.read()).decode("utf-8", errors="ignore")
soup = BeautifulSoup(html, "html.parser")

for leader_box in soup.find_all(class_=re.compile(r'team|leader|col|member', re.I)):
    name_el = leader_box.find(["h2", "h3", "h4"])
    if name_el and any(role in leader_box.text for role in ["Founder", "Partner", "CEO", "Director"]):
        name = name_el.get_text(strip=True).encode('ascii', errors='replace').decode()
        text = leader_box.get_text(" | ", strip=True).encode('ascii', errors='replace').decode()
        print(f"Name: {name}")
        print(f"  Summary: {text[:250]}\n")
