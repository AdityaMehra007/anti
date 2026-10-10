import urllib.request
import re
import json

url = "https://careers.walmart.com/us/en/results?q=India"
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
            print("phApp keys:", data.keys())
            
        # Search for jobs array or total jobs count
        total_hits = re.findall(r'\"totalHits\":\s*(\d+)', html)
        print("Total hits:", total_hits)
        
        # Look for API urls
        api_urls = re.findall(r'https?://[^\s"\'<>]+(?:api|jobs|search|widgets)[^\s"\'<>]*', html)
        print("API urls found:", set(api_urls[:10]))
        
        with open("scratch/walmart_page.html", "w", encoding="utf-8") as f:
            f.write(html)
            
except Exception as e:
    print("Error:", e)
