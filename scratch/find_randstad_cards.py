from bs4 import BeautifulSoup
import re

with open("scratch/randstad_bangalore.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("Title:", soup.title.string.strip() if soup.title else "No title")

# Check for links with /jobs/
job_links = set()
for a in soup.find_all("a", href=True):
    href = a["href"]
    if "/jobs/" in href and href != "/jobs/" and not href.startswith("/jobs/re-") and not href.startswith("/jobs/ci-"):
        job_links.add((a.get_text(strip=True), href))

print(f"Candidate job links ({len(job_links)}):")
for t, h in list(job_links)[:15]:
    print(f"  [{t}] -> {h}")

# Check for headings
print("\nHeadings (h1, h2, h3):")
for h in soup.find_all(["h1", "h2", "h3"])[:15]:
    t = h.get_text(strip=True)
    if t:
        print(f"  {h.name}: {t[:100]}")
