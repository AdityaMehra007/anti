import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://careers.cred.club/openings"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"HTML Length: {len(html)}")
        
        # Check for Lever or Greenhouse or API links
        if "lever.co" in html.lower():
            print("Lever detected!")
        if "greenhouse.io" in html.lower():
            print("Greenhouse detected!")
            
        # check for Next.js or JSON data
        json_matches = re.findall(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
        if json_matches:
            print("Found __NEXT_DATA__!")
            data = json.loads(json_matches[0])
            with open("scratch/cred_next_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print("Saved cred_next_data.json")
            
        # check any job links in HTML
        job_links = re.findall(r'href="([^"]*(?:openings/[^"]*|jobs\.lever\.co/[^"]*|boards\.greenhouse\.io/[^"]*))"', html)
        print("Job links found:", len(job_links))
        for l in set(job_links[:10]):
            print(" ", l)
except Exception as e:
    print(f"Error: {e}")
