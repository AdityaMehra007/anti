import urllib.request
import ssl
import re

url = "https://jobs.myntra.com/main.dart.js"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, context=ctx).read().decode("utf-8", errors="ignore")

# Find occurrences of $.i6()
matches = list(re.finditer(re.escape(r'$.i6()'), content))
print(f"Total $.i6() matches: {len(matches)}")
paths = set()
for m in matches:
    snippet = content[m.start():m.start()+150]
    m_path = re.search(r'\$\.i6\(\)\s*\+\s*["\']([^"\']+)["\']', snippet)
    if m_path:
        paths.add(m_path.group(1))

print("Found $.i6() paths:")
for p in sorted(paths):
    print("  ", p)

# Find occurrences of $.IY()
matches_iy = list(re.finditer(re.escape(r'$.IY()'), content))
print(f"\nTotal $.IY() matches: {len(matches_iy)}")
paths_iy = set()
for m in matches_iy:
    snippet = content[m.start():m.start()+150]
    m_path = re.search(r'\$\.IY\(\)\s*\+\s*["\']([^"\']+)["\']', snippet)
    if m_path:
        paths_iy.add(m_path.group(1))

print("Found $.IY() paths:")
for p in sorted(paths_iy):
    print("  ", p)
