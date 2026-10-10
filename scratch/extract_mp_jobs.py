from bs4 import BeautifulSoup
import json
import re

with open("scratch/michaelpage_bangalore.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Look for pagination or total count
# e.g., class with total, count, pager, etc.
text_all = soup.get_text()
for line in text_all.split("\n"):
    line_clean = line.strip()
    if any(k in line_clean.lower() for k in ["job", "found", "showing", "of", "results"]) and any(c.isdigit() for c in line_clean):
        if len(line_clean) < 100:
            print("Found line:", line_clean)

# Look for cards or list items
# Let's find elements that contain /job-detail/
job_cards = []
seen_urls = set()

for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.startswith("/job-detail/") and href not in seen_urls:
        seen_urls.add(href)
        # Find the card container
        card = a.find_parent("li") or a.find_parent("div", class_=re.compile(r'job|card|row|item', re.I))
        title = a.get_text(strip=True)
        if not title or title.lower() == "view job":
            continue
            
        card_text = card.get_text(" | ", strip=True) if card else ""
        job_cards.append({
            "title": title,
            "url": "https://www.michaelpage.co.in" + href,
            "summary": card_text
        })

print(f"\nTotal distinct job cards found: {len(job_cards)}")
for i, j in enumerate(job_cards, 1):
    print(f"\n{i}. {j['title']}")
    print(f"   URL: {j['url']}")
    # print snippet of summary
    lines = [p.strip() for p in j['summary'].split("|") if p.strip() and p.strip() != j['title'] and p.strip().lower() != "view job"]
    print(f"   Details: {' | '.join(lines[:6])}")
