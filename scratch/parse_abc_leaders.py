from bs4 import BeautifulSoup
import re

with open("scratch/abc_exec_search_decoded.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

leaders = []
for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.startswith("mailto:") and "@abcconsultants.in" in href:
        email = href.replace("mailto:", "").strip()
        # Find associated profile link or name
        parent = a.find_parent(["div", "li", "article"])
        text = parent.get_text(" | ", strip=True) if parent else ""
        leaders.append((email, text))

for email, text in set(leaders):
    parts = [p.strip() for p in text.split("|") if p.strip()]
    name = parts[0] if parts else email.split("@")[0].replace(".", " ").title()
    title = parts[1] if len(parts) > 1 else ""
    print(f"Leader: {name} ({email}) - {title}")
