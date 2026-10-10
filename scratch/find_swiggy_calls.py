import re

with open("scratch/inspect_swiggy_bundle.py") as f:
    pass

import urllib.request
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://careers.swiggy.in/assets/index-CbfQuJ9d.js"
with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), context=ctx) as resp:
    js = resp.read().decode('utf-8', errors='ignore')

# Search for keywords
for word in ["darwinbox", "greenhouse", "lever", "workday", "eightfold", "smartrecruiters", "phenom", "keka"]:
    if word in js.lower():
        print(f"Found ATS keyword: {word}")

# Search for fetch / axios endpoints
fetch_calls = re.findall(r'fetch\([\"\'`]([^\"\'`]+)[\"\'`]', js)
print("fetch() calls:", fetch_calls)

axios_calls = re.findall(r'axios\.[a-z]+\([\"\'`]([^\"\'`]+)[\"\'`]', js)
print("axios calls:", axios_calls)

# Look for URL strings with job
job_urls = re.findall(r'[\"\'`]([^\s\"\'`]*job[^\s\"\'`]*)[\"\'`]', js)
print("Job URL strings:", set(job_urls[:15]))
