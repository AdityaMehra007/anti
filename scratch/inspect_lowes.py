import urllib.request
import re
import json

url = "https://talent.lowes.com/in/en/c/corporate-jobs"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"Status: {resp.status}, HTML length: {len(html)}")
        
        # Look for Phenom People data, phApp, or api endpoints
        ph_match = re.search(r'phApp\.pageData\s*=\s*({.*?});', html, re.S)
        if ph_match:
            print("Found phApp.pageData!")
            data = json.loads(ph_match.group(1))
            print("phApp keys:", list(data.keys()))
            with open("scratch/lowes_pagedata.json", "w", encoding="utf-8") as out:
                json.dump(data, out, indent=2)
                
        # Look for refNum or job postings
        jobs_match = re.findall(r'\"reqId\":\s*\"([^\"]+)\"', html)
        print("reqIds found in HTML:", len(jobs_match), jobs_match[:5])
        
        # Look for totalHits
        hits = re.findall(r'\"totalHits\":\s*(\d+)', html)
        print("Total hits:", hits)
        
        with open("scratch/lowes_page.html", "w", encoding="utf-8") as f:
            f.write(html)
except Exception as e:
    print("Error:", e)
