import re
import json

with open("scratch/michaelpage_bangalore.html", "r", encoding="utf-8") as f:
    html = f.read()

print("HTML Length:", len(html))

# Look for total jobs count
count_matches = re.findall(r'(\d[\d,]*)\s*(?:jobs?|vacancies|results)', html, re.IGNORECASE)
print("Count matches:", count_matches[:10])

# Look for job card articles or items
job_articles = re.findall(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
print("Article tags found:", len(job_articles))

# Look for job links: /job-detail/
job_links = set(re.findall(r'href=["\'](/job-detail/[^"\']+)["\']', html))
print(f"Job links found: {len(job_links)}")
for l in list(job_links)[:10]:
    print("  ", l)

# Look for json-ld
json_lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
print(f"JSON-LD blocks: {len(json_lds)}")
for i, jld in enumerate(json_lds):
    try:
        parsed = json.loads(jld)
        print(f"  JSON-LD {i} type: {parsed.get('@type') if isinstance(parsed, dict) else [x.get('@type') for x in parsed if isinstance(x, dict)]}")
        if isinstance(parsed, dict) and parsed.get('@type') == 'ItemList':
            items = parsed.get('itemListElement', [])
            print(f"  ItemList items count: {len(items)}")
            with open("scratch/michaelpage_itemlist.json", "w", encoding="utf-8") as out:
                json.dump(parsed, out, indent=2)
    except Exception as e:
        print(f"  JSON-LD {i} error: {e}")
