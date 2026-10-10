import urllib.request
import re

url = "https://www.meesho.io/_next/static/chunks/pages/jobs-721b32edb85df57d.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        print(f"Downloaded jobs chunk: {len(content)} bytes")
        
        # Look for fetch / axios / urls / api
        urls = re.findall(r'https?://[^\s"\'`<>]+', content)
        print("URLs found in chunk:", set(urls))
        
        # Look for strings containing api or job or greenhouse etc
        api_matches = re.findall(r'["\'](/[^"\']*api[^"\']*)["\']', content, re.I)
        print("API paths:", set(api_matches))
        
        # Find fetch or axios calls
        fetch_matches = re.findall(r'fetch\([^\)]+\)', content)
        print("Fetch matches:", fetch_matches[:10])
        
        # Search for any endpoint pattern
        endpoints = re.findall(r'["\'](https?://[^"\']+meesho[^"\']*)["\']', content)
        print("Meesho endpoints:", set(endpoints))
        
        with open("scratch/meesho_jobs_chunk.js", "w", encoding="utf-8") as f:
            f.write(content)
except Exception as e:
    print("Error:", e)
