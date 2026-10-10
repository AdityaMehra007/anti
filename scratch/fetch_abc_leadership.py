import urllib.request
import ssl
import gzip
from bs4 import BeautifulSoup
import re

url = "https://www.abcconsultants.in/i-am-seeking-leadership-roles/"
ctx = ssl._create_unverified_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Encoding": "gzip, deflate"
}

req = urllib.request.Request(url, headers=headers)
try:
    res = urllib.request.urlopen(req, context=ctx)
    content = res.read()
    if res.headers.get("Content-Encoding") == "gzip":
        html = gzip.decompress(content).decode("utf-8", errors="ignore")
    else:
        html = content.decode("utf-8", errors="ignore")
    print("Page fetched! Length:", len(html))
    soup = BeautifulSoup(html, "html.parser")
    print("Title:", soup.title.string.encode('ascii', errors='replace').decode() if soup.title else "No title")
    
    # Check form fields
    form = soup.find("form")
    if form:
        print("Form action:", form.get("action"))
        for inp in form.find_all(["input", "select", "textarea"]):
            name = inp.get("name")
            typ = inp.get("type", inp.name)
            placeholder = inp.get("placeholder", "")
            print(f"  Field: {name} (type={typ}, placeholder={placeholder})")
            
    # Check text content
    paras = [p.get_text(strip=True).encode('ascii', errors='replace').decode() for p in soup.find_all("p") if p.get_text(strip=True)]
    print("\nParagraphs:")
    for p in paras[:8]:
        print("  -", p[:120])
except Exception as e:
    print("ERROR:", e)
