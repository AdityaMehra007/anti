import re

with open("scratch/search_spire.py", "r") as f:
    pass

import urllib.request
import ssl

url = "https://jobs.myntra.com/main.dart.js"
ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, context=ctx).read().decode("utf-8", errors="ignore")

# Find where $.T7 is defined or what $.T7 returns
for m in re.finditer(r'T7\(\)', content):
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 200)
    print("Match T7():", content[start:end])

# Search for /v1/p or searchJob or getJobs or jobs
for m in re.finditer(r'v1/p', content):
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 200)
    print("Match v1/p:", content[start:end])

# Search for tenant name / client name / myntra in lowercase
for m in re.finditer(r'clientName|tenantId|companyId|clientId', content, re.IGNORECASE):
    start = max(0, m.start() - 50)
    end = min(len(content), m.end() + 100)
    print("Match tenant/client:", content[start:end])
    break
