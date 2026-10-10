import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://flipkart.turbohire.co/dashboardv2?orgId=4d757ba0-3d57-448a-b82c-238ed87ac90f&type=0"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"HTML Length: {len(html)}")
        
        # Look for API endpoints or embedded jobs in script tags
        scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
        print("Scripts found:", len(scripts))
        for s in scripts[:5]:
            print(" ", s)
            
        # Look for inline json or api endpoints
        apis = re.findall(r'https?://[^\s"\'<>]+(?:api|turbohire|jobs)[^\s"\'<>]*', html)
        print("APIs / links found:", set(apis[:10]))
except Exception as e:
    print(f"Error: {e}")
