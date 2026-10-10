import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.ibm.com/in-en/careers/search?field_keyword_18%5B0%5D=Entry%20Level&source=WEB_ENTRY_INDIA"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"HTML Length: {len(html)}")
        
        # Look for job links or API endpoints
        # IBM often uses BrassRing, Eightfold, or custom Drupal / Next.js / JSON payload
        json_matches = re.findall(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
        if json_matches:
            print("Found __NEXT_DATA__!")
            data = json.loads(json_matches[0])
            with open("scratch/ibm_next_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print("Saved __NEXT_DATA__")
        else:
            print("No __NEXT_DATA__, checking other scripts or patterns")
            links = re.findall(r'href="([^"]*careers[^"]*|[^"]*job[^"]*)"', html)
            print("Sample links:", links[:10])
            
            # Check for requisition IDs or job titles
            req_matches = re.findall(r'([0-9]{5,8}[A-Z]{0,2}|[A-Z]{2,4}[0-9]{4,8})', html)
            print("Sample IDs:", req_matches[:10])
except Exception as e:
    print(f"Error: {e}")
