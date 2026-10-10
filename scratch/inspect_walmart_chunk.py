import urllib.request
import re

url = "https://i5.walmartimages.com/dfw/6019e67e-4d91/b4d18730-9880-4875-906b-0d9cb9d9c03b/v2/_next/static/chunks/pages/%5Bcountry%5D/%5Blang%5D/results-05dea8be46ef0788.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        print(f"Downloaded results chunk: {len(content)} bytes")
        
        # Look for API endpoints, URLs, fetch / axios
        urls = re.findall(r'https?://[^\s"\'`<>]+', content)
        print("URLs in chunk:", set(urls))
        
        paths = re.findall(r'["\'](/[^"\'`\s]+(?:api|jobs|search)[^"\'`\s]*)["\']', content)
        print("API paths:", set(paths))
        
        # Look for endpoint templates
        templates = re.findall(r'[`"\']([^`"\']*(?:search|jobs)[^`"\']*)[`"\']', content)
        valid_templates = [t for t in templates if len(t) < 80 and "/" in t]
        print("Templates matching search/jobs:", valid_templates[:15])
except Exception as e:
    print("Error:", e)
