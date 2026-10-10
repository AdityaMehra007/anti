from bs4 import BeautifulSoup
import json
import re

with open("scratch/wellfound_bangalore.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

next_data = soup.find("script", id="__NEXT_DATA__")
if next_data:
    data = json.loads(next_data.string)
    apollo = data.get("props", {}).get("pageProps", {}).get("apolloState", {})
    print("Apollo state keys count:", len(apollo))
    with open("scratch/wellfound_blr_apollo.json", "w", encoding="utf-8") as out:
        json.dump(apollo, out, indent=2)
    print("Saved scratch/wellfound_blr_apollo.json")

    # Inspect types of objects in apolloState
    type_counts = {}
    job_listings = []
    startups = []
    for k, v in apollo.items():
        if isinstance(v, dict):
            t = v.get("__typename", "Unknown")
            type_counts[t] = type_counts.get(t, 0) + 1
            if t in ["JobListing", "Job", "JobListingSearchResult"]:
                job_listings.append(v)
            elif t in ["Startup", "Company"]:
                startups.append(v)

    print("\nApollo Object Types:")
    for t, cnt in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"  {t}: {cnt}")

    print(f"\nJob listings found: {len(job_listings)}")
    print(f"Startups found: {len(startups)}")
    if job_listings:
        print("Sample job listing keys:", list(job_listings[0].keys()))
        print("Sample job listing:", job_listings[0])
    if startups:
        print("Sample startup keys:", list(startups[0].keys()))
        print("Sample startup:", startups[0].get("name"))
