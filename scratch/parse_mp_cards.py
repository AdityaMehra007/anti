import re
from bs4 import BeautifulSoup
import json

with open("scratch/michaelpage_bangalore.html", "r", encoding="utf-8") as f:
    html = f.read()

# Look for total count in text
# Let's search for "Showing", "results", "of", "jobs"
snippets = re.findall(r'([^<>\n\r]{0,50}(?:jobs?|results?|vacancies)[^<>\n\r]{0,50})', html, re.IGNORECASE)
for s in snippets[:15]:
    if any(c.isdigit() for c in s):
        print("Count snippet:", s.strip())

# Find job cards
# Job links: href="/job-detail/..."
job_card_blocks = []
# Let's inspect surrounding HTML of href="/job-detail/"
matches = list(re.finditer(r'<a[^>]*href=["\'](/job-detail/[^"\']+)["\'][^>]*>(.*?)</a>', html, re.DOTALL))
print(f"Total matching <a> tags for job-detail: {len(matches)}")

for m in matches[:10]:
    url = m.group(1)
    text = re.sub(r'<[^>]+>', ' ', m.group(2)).strip()
    print(f"URL: {url}")
    print(f"  Title: {text}")
