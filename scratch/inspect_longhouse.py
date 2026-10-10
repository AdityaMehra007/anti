from bs4 import BeautifulSoup
import re

with open("scratch/longhouse_home.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

print("Title:", soup.title.string.strip() if soup.title else "No title")

# Look for links
links = set()
for a in soup.find_all("a", href=True):
    href = a["href"]
    text = a.get_text(strip=True)
    if "longhouse.in" in href or href.startswith("/") or href.startswith("mailto:"):
        links.add((text, href))

print(f"\nTotal internal/mailto links: {len(links)}")
for text, href in sorted(links):
    text_clean = text.encode('ascii', errors='replace').decode()
    print(f"  [{text_clean}] -> {href}")

# Headings
print("\nHeadings:")
for h in soup.find_all(["h1", "h2", "h3", "h4"]):
    t = h.get_text(strip=True)
    if t:
        print(f"  {h.name}: {t.encode('ascii', errors='replace').decode()}")
