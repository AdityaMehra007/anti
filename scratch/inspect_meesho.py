import urllib.request
import re

req = urllib.request.Request('https://www.meesho.io/jobs', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

scripts = re.findall(r'src="([^"]+\.js)"', html)
print(f"Scripts found: {len(scripts)}")
for s in scripts:
    print(s)

# Also check for API endpoints or greenhouse / lever / darwinbox / etc.
print("\nChecking for common ATS tokens:")
for pattern in ["greenhouse", "lever", "workday", "smartrecruiters", "darwinbox", "turbohire", "ashby", "api"]:
    matches = re.findall(r'[^"\'\s<>]*' + pattern + r'[^"\'\s<>]*', html, re.I)
    print(f"{pattern}: {len(matches)} matches -> {matches[:5]}")
