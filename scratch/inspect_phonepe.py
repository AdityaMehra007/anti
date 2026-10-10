import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.phonepe.com/careers/job-openings/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"HTML Length: {len(html)}")
        
        # Look for greenhouse, lever, darwinbox, or custom apis
        if "greenhouse" in html.lower():
            print("Greenhouse detected!")
        if "lever" in html.lower():
            print("Lever detected!")
            
        # check for json data
        json_matches = re.findall(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
        if json_matches:
            print("Found __NEXT_DATA__!")
            data = json.loads(json_matches[0])
            with open("scratch/phonepe_next_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print("Saved phonepe_next_data.json")
            
        # check any script endpoints or job links
        job_links = re.findall(r'href="([^"]*(?:careers/job|job-openings/[^"]*|greenhouse.io/[^"]*))"', html)
        print("Job links found:", len(job_links))
        for l in job_links[:10]:
            print(" ", l)
except Exception as e:
    print(f"Error: {e}")
