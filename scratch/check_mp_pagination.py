from bs4 import BeautifulSoup
import re

with open("scratch/michaelpage_bangalore.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

pager = soup.find(class_=re.compile(r'pager|pagination', re.I))
if pager:
    print("Pager found:")
    print(pager.prettify())
else:
    print("No pager found by class. Checking links with 'page=':")
    for a in soup.find_all("a", href=True):
        if "page=" in a["href"]:
            print("  Pagination link:", a["href"], a.get_text(strip=True))

# Check any element containing 'results' or 'showing'
for el in soup.find_all(string=re.compile(r'(?:showing|found|results|\bof\b)', re.I)):
    parent = el.parent
    text = parent.get_text(strip=True)
    if any(c.isdigit() for c in text) and len(text) < 80:
        print("Count text:", text)
