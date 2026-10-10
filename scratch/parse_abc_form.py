from bs4 import BeautifulSoup

with open("scratch/fetch_abc_leadership.py", "r") as f:
    pass

import urllib.request
import ssl
import gzip

url = "https://www.abcconsultants.in/i-am-seeking-leadership-roles/"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip, deflate"})
res = urllib.request.urlopen(req, context=ctx)
html = gzip.decompress(res.read()).decode("utf-8", errors="ignore")
soup = BeautifulSoup(html, "html.parser")

for form_group in soup.find_all(class_=lambda c: c and "quform-element" in c):
    label = form_group.find("label")
    label_text = label.get_text(strip=True) if label else "No label"
    inp = form_group.find(["input", "select", "textarea"])
    name = inp.get("name") if inp else "None"
    options = [opt.get_text(strip=True) for opt in form_group.find_all("option")] if form_group.find("select") else []
    
    print(f"Label: {label_text} -> name: {name}")
    if options:
        print(f"  Options: {options[:6]}")
