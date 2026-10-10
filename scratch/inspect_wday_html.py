import urllib.request
import re

url = "https://walmart.wd504.myworkdayjobs.com/Walmart_External_Careers?locationCountry=bc33aa3152ec42d49cf5f4d92416f461"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print("Page length:", len(html))
        # look for cxs or api or client
        matches = re.findall(r'\"/wday/cxs/[^\"]+\"', html)
        print("CXS matches:", matches)
        # search for appData or client config
        configs = re.findall(r'window\.workday\s*=\s*({.*?});', html, re.S)
        if configs:
            print("Found window.workday!")
        else:
            urls = re.findall(r'https?://[^\s"\'<>]+/wday/[^\s"\'<>]+', html)
            print("Wday URLs:", urls)
            
        with open("scratch/walmart_workday.html", "w", encoding="utf-8") as out:
            out.write(html)
except Exception as e:
    print("Error:", e)
