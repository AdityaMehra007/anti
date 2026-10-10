import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://careers.swiggy.in/explore-jobs"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"HTML Length: {len(html)}")
        
        # Look for platform cues (darwinbox, phenom, greenhouse, lever, workday)
        for platform in ["darwinbox", "phenom", "greenhouse", "lever", "workday", "eightfold"]:
            if platform in html.lower():
                print(f"Detected: {platform}!")
                
        # Look for API endpoints or json scripts
        apis = re.findall(r'https?://[^\s"\'<>]+(?:api|job|career)[^\s"\'<>]*', html)
        print("APIs found:", set(apis[:10]))
        
        # Check __NEXT_DATA__ or similar
        json_matches = re.findall(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
        if json_matches:
            print("Found __NEXT_DATA__!")
            data = json.loads(json_matches[0])
            with open("scratch/swiggy_next_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print("Saved swiggy_next_data.json")
            
        # check script tags
        scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
        print("Scripts found:", len(scripts))
        for s in scripts[:5]:
            print(" ", s)
except Exception as e:
    print(f"Error: {e}")
