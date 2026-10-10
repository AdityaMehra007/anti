from bs4 import BeautifulSoup
import re
import json

with open("scratch/abc_exec_search_decoded.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("Title:", soup.title.string if soup.title else "No title")

# Look for links on the page
links = set()
for a in soup.find_all("a", href=True):
    href = a["href"]
    text = a.get_text(strip=True)
    if any(k in href.lower() or k in text.lower() for k in ["job", "career", "search", "bangalore", "bengaluru", "contact", "submit", "cv", "resume", "practice", "leader"]):
        links.add((text, href))

print(f"\nRelevant links ({len(links)}):")
for text, href in sorted(links):
    print(f"  [{text}] -> {href}")

# Find main content headings and paragraphs
print("\nHeadings:")
for h in soup.find_all(["h1", "h2", "h3"]):
    text = h.get_text(strip=True)
    if text:
        print(f"  {h.name}: {text}")
