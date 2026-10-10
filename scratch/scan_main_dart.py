import urllib.request
import ssl
import re

url = "https://jobs.myntra.com/main.dart.js"
ctx = ssl._create_unverified_context()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Range": "bytes=0-1048576" # Read first 1MB or stream search
}

# Let's stream and search for URLs and endpoints
req = urllib.request.Request(url, headers={"User-Agent": headers["User-Agent"]})
print("Opening main.dart.js...")
res = urllib.request.urlopen(req, context=ctx)

chunk_size = 512 * 1024
total = 0
found_urls = set()
found_apis = set()

while total < 15 * 1024 * 1024:
    chunk = res.read(chunk_size)
    if not chunk:
        break
    total += len(chunk)
    text = chunk.decode("utf-8", errors="ignore")
    
    # search for https:// or api patterns
    matches = re.findall(r'https?://[a-zA-Z0-9_\.\-]+(?::\d+)?(?:/[a-zA-Z0-9_\.\-\?=%&;~]*)?', text)
    for m in matches:
        if any(term in m.lower() for term in ["myntra", "iexchange", "career", "job", "darwinbox", "oracle", "workday", "api"]):
            found_urls.add(m)
            
    # search for /api/ patterns
    api_matches = re.findall(r'["\'](/api/[a-zA-Z0-9_\.\-/]+)["\']', text)
    for m in api_matches:
        found_apis.add(m)

    if len(found_urls) > 50:
        break

print(f"Total read: {total} bytes")
print("\n--- FOUND RELEVANT URLS ---")
for u in sorted(found_urls):
    print(u)

print("\n--- FOUND API PATHS ---")
for a in sorted(found_apis):
    print(a)
