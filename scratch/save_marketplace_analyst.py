import json
import re
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

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
    desc = re.sub(r'<[^>]+>', '\n', job_detail.get("description", ""))
    
    with open("scratch/lowes_marketplace_analyst.txt", "w", encoding="utf-8") as out:
        out.write(f"Title: {job_detail.get('title')}\n")
        out.write(f"Req ID: {job_detail.get('reqId')}\n")
        out.write(f"Location: {job_detail.get('city')}, {job_detail.get('state')}, {job_detail.get('country')}\n\n")
        out.write(desc)
    print("Saved to scratch/lowes_marketplace_analyst.txt successfully!")
