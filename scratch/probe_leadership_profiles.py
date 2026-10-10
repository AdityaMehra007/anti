from bs4 import BeautifulSoup
import re

with open("scratch/abc_exec_search_decoded.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

for link_href in [
    "https://www.abcconsultants.in/murali-mohan/",
    "https://www.abcconsultants.in/ratna-gupta/",
    "https://www.abcconsultants.in/upasana-agarwal/",
    "https://www.abcconsultants.in/shiv-agrawal/"
]:
    # Let's fetch one profile to see practice ownership
    import urllib.request, ssl, gzip
    ctx = ssl._create_unverified_context()
    req = urllib.request.Request(link_href, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip, deflate"})
    try:
        res = urllib.request.urlopen(req, context=ctx)
        html = gzip.decompress(res.read()).decode("utf-8", errors="ignore")
        p_soup = BeautifulSoup(html, "html.parser")
        name = p_soup.find("h1").get_text(strip=True) if p_soup.find("h1") else link_href.split("/")[-2]
        paras = [p.get_text(strip=True) for p in p_soup.find_all("p") if p.get_text(strip=True)]
        print(f"Name: {name}")
        for p in paras[:3]:
            print("  ", p[:150].encode('ascii', errors='replace').decode())
        print()
    except Exception as e:
        print("Error:", e)
