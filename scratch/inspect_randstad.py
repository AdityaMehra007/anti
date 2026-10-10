import json
import re
from bs4 import BeautifulSoup

with open("scratch/randstad_bangalore.html", "r", encoding="utf-8") as f:
    html = f.read()

print("HTML Length:", len(html))

# Look for JSON-LD schemas
json_lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
print(f"JSON-LD blocks found: {len(json_lds)}")

job_postings = []
for i, block in enumerate(json_lds):
    try:
        data = json.loads(block)
        if isinstance(data, dict):
            if data.get("@type") == "JobPosting":
                job_postings.append(data)
            elif data.get("@type") == "ItemList":
                items = data.get("itemListElement", [])
                print(f"ItemList block {i} with {len(items)} items")
                for item in items:
                    if isinstance(item, dict) and item.get("@type") == "JobPosting":
                        job_postings.append(item)
                    elif isinstance(item, dict) and "item" in item and isinstance(item["item"], dict):
                        job_postings.append(item["item"])
        elif isinstance(data, list):
            for d in data:
                if isinstance(d, dict) and d.get("@type") == "JobPosting":
                    job_postings.append(d)
    except Exception as e:
        pass

print(f"\nExtracted JobPosting objects: {len(job_postings)}")

if job_postings:
    with open("scratch/randstad_job_postings.json", "w", encoding="utf-8") as out:
        json.dump(job_postings, out, indent=2)
    print("Saved scratch/randstad_job_postings.json")
    print("\nSample Job:")
    print("  Title:", job_postings[0].get("title"))
    print("  Employer:", job_postings[0].get("hiringOrganization", {}).get("name"))
    print("  URL:", job_postings[0].get("url"))
    print("  Date:", job_postings[0].get("datePosted"))
    print("  Location:", job_postings[0].get("jobLocation"))
else:
    # Check HTML markup for job card links
    soup = BeautifulSoup(html, "html.parser")
    job_links = set(re.findall(r'href=["\'](/jobs/[^"\']+_\d+/)["\']', html))
    print(f"Job links matching pattern: {len(job_links)}")
    for l in list(job_links)[:5]:
        print(" ", l)
