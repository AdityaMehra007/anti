import json
import re

with open("scratch/walmart_page.html", "r", encoding="utf-8") as f:
    html = f.read()

m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
if m:
    data = json.loads(m.group(1))
    print("Keys in __NEXT_DATA__:", data.keys())
    pageProps = data.get("props", {}).get("pageProps", {})
    with open("scratch/walmart_pageprops.json", "w", encoding="utf-8") as out:
        json.dump(pageProps, out, indent=2)
    print("Saved scratch/walmart_pageprops.json! Keys:", pageProps.keys())
else:
    print("No __NEXT_DATA__ found")
