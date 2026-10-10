import urllib.request
import ssl
import gzip
import re
from bs4 import BeautifulSoup

ctx = ssl._create_unverified_context()
headers = {"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip, deflate"}

for path in ["candidates/", "contact-us/", "about-us/"]:
    url = f"https://longhouse.in/{path}"
    req = urllib.request.Request(url, headers=headers)
    try:
        res = urllib.request.urlopen(req, context=ctx)
        html = gzip.decompress(res.read()).decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")
        print(f"\n================= {path} =================")
        print("Title:", soup.title.string.strip() if soup.title else "")
        emails = set(re.findall(r'[a-zA-Z0-9_\.\+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+', html))
        print("Emails found:", emails)
        form = soup.find("form")
        if form:
            print("Form action:", form.get("action"))
            for inp in form.find_all(["input", "select", "textarea"]):
                print(f"  Field: {inp.get('name')} (type={inp.get('type', inp.name)}, placeholder={inp.get('placeholder', '')})")
        # Look for headings and paras
        for h in soup.find_all(["h1", "h2", "h3"]):
            t = h.get_text(strip=True).encode('ascii', errors='replace').decode()
            if t:
                print(f"  {h.name}: {t}")
        paras = [p.get_text(strip=True).encode('ascii', errors='replace').decode() for p in soup.find_all("p") if p.get_text(strip=True)]
        for p in paras[:6]:
            print("  Para:", p[:140])
    except Exception as e:
        print(f"Error on {path}: {e}")
