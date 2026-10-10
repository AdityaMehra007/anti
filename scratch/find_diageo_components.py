with open("scratch/diageo_page.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# Look for iframes
iframes = re.findall(r'<iframe[^>]*src=["\']([^"\']+)["\']', html, re.IGNORECASE)
print("Iframes found:", iframes)

# Look for data- attributes or job-search components
components = re.findall(r'data-[a-zA-Z0-9_\-]+=["\'][^"\']*job[^"\']*["\']', html, re.IGNORECASE)
print("Job data attributes:", components[:10])

# Look for any form or search input
inputs = re.findall(r'<input[^>]*name=["\']([^"\']+)["\']', html)
print("Inputs found:", inputs)

# Look for occurrences of "country" or "India" or "Bengaluru" or "Bangalore"
for term in ["Bengaluru", "Bangalore", "country=India"]:
    matches = [m.start() for m in re.finditer(term, html, re.IGNORECASE)]
    print(f"Term '{term}': {len(matches)} occurrences")
    for m in matches[:3]:
        print("  Snippet:", html[max(0, m-100):min(len(html), m+200)])
