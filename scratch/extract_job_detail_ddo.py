import json
import re

with open("scratch/inspect_lowes_desc.py") as f:
    pass

import urllib.request
url = "https://talent.lowes.com/in/en/job/JR-02672638"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

pos = html.find("phApp.ddo =")
if pos != -1:
    raw = html[pos + len("phApp.ddo = "):]
    decoder = json.JSONDecoder()
    obj, _ = decoder.raw_decode(raw)
    job_detail = obj.get("jobDetail", {}).get("data", {}).get("job", {})
    print("Job Title:", job_detail.get("title"))
    print("Job ReqId:", job_detail.get("reqId"))
    print("Locations:", job_detail.get("city"), job_detail.get("state"), job_detail.get("country"))
    print("Description snippet:")
    desc = re.sub(r'<[^>]+>', '\n', job_detail.get("description", ""))
    lines = [l.strip() for l in desc.split("\n") if l.strip()]
    for l in lines[:30]:
        print("  ", l)
