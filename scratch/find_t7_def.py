import urllib.request
import ssl
import re

url = "https://jobs.myntra.com/main.dart.js"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, context=ctx).read().decode("utf-8", errors="ignore")

# Let's find definition of T7
# In dart2js, r($, "T7", ...) or T7: function or similar
for m in re.finditer(r'r\(\$,"T7"', content):
    start = max(0, m.start() - 50)
    end = min(len(content), m.end() + 200)
    print("Match r($, 'T7'):", content[start:end])

# Search for "T7()", or find where T7 is assigned
for m in re.finditer(r'T7=|\.T7\s*=', content):
    start = max(0, m.start() - 50)
    end = min(len(content), m.end() + 200)
    print("Match T7 assignment:", content[start:end])

# Also search for 'banner_image.jpg' context
idx = content.find("banner_image.jpg")
if idx != -1:
    print("\n--- Context around banner_image.jpg ---")
    print(content[idx-300:idx+300])
