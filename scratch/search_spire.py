import urllib.request
import ssl
import re

url = "https://jobs.myntra.com/main.dart.js"
ctx = ssl._create_unverified_context()
headers = {"User-Agent": "Mozilla/5.0"}

req = urllib.request.Request(url, headers=headers)
res = urllib.request.urlopen(req, context=ctx)
content = res.read().decode("utf-8", errors="ignore")

print("Content length:", len(content))

# Look for spire2grow or iexchange or baseUrl
spire_matches = set(re.findall(r'https?://[a-zA-Z0-9_\.\-]+(?::\d+)?/[a-zA-Z0-9_\.\-/]*spire[a-zA-Z0-9_\.\-/]*', content))
print("Spire matches:", spire_matches)

iexchange_matches = set(re.findall(r'https?://[a-zA-Z0-9_\.\-]+(?::\d+)?/[a-zA-Z0-9_\.\-/]*iexchange[a-zA-Z0-9_\.\-/]*', content))
print("Iexchange matches:", iexchange_matches)

# Look for baseUrl or api strings
for match in re.finditer(r'baseUrl|apiEndpoint|hostUrl', content, re.IGNORECASE):
    start = max(0, match.start() - 100)
    end = min(len(content), match.end() + 100)
    print("Context around match:", content[start:end])
    break

# Look for occurrences of spire2grow
for match in re.finditer(r'spire2grow', content):
    start = max(0, match.start() - 150)
    end = min(len(content), match.end() + 150)
    print("Context around spire2grow:\n", content[start:end])
