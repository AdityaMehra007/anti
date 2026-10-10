from bs4 import BeautifulSoup
import re

with open("scratch/abc_exec_search_decoded.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

contact_links = []
for a in soup.find_all("a", href=True):
    href = a["href"]
    text = a.get_text(strip=True)
    if "abcconsultants.in" in href:
        contact_links.append((text, href))

for t, h in set(contact_links):
    print(f"[{t}] -> {h}")
