import re
import json
from bs4 import BeautifulSoup

with open("scratch/wellfound_jobs.html", "r", encoding="utf-8") as f:
    html = f.read()

print("HTML Length:", len(html))

soup = BeautifulSoup(html, "html.parser")
print("Title:", soup.title.string.strip() if soup.title else "No title")

# Check for __NEXT_DATA__
next_data = soup.find("script", id="__NEXT_DATA__")
if next_data:
    print("Found __NEXT_DATA__! Length:", len(next_data.string))
    try:
        data = json.loads(next_data.string)
        print("Page props keys:", list(data.get("props", {}).get("pageProps", {}).keys()))
        with open("scratch/wellfound_next_data.json", "w", encoding="utf-8") as out:
            json.dump(data, out, indent=2)
        print("Saved scratch/wellfound_next_data.json")
    except Exception as e:
        print("Error parsing JSON:", e)
else:
    print("No __NEXT_DATA__ found. Checking other script tags...")
    for s in soup.find_all("script"):
        if s.string and "apollo" in s.string.lower():
            print("Found Apollo script tag!")
