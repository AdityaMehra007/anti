import urllib.request
import json

job_paths = {
    "AIOC-S01664213-1": "/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1",
    "AIOC-S01664212-1": "/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664212-1",
    "AIOC-S01670871-1": "/job/Bengaluru/Procure-to-Pay-Operations-New-Associate_AIOC-S01670871-1",
    "AIOC-S01669615-1": "/job/Bengaluru/Sales-Operations-New-Associate_AIOC-S01669615-1",
    "AIOC-S01668350-1": "/job/Bengaluru/Trust---Safety-New-Associate_AIOC-S01668350-1",
    "AIOC-S01667647-1": "/job/Bengaluru/Regulatory-Compliance-New-Associate_AIOC-S01667647-1",
    "AIOC-S01663367-1": "/job/Bengaluru/HR-Service-Delivery-New-Associate_AIOC-S01663367-1",
    "AIOC-S01665940-1": "/job/Bengaluru/Customer-Contact-Comms-Associate-Messaging_AIOC-S01665940-1",
    "AIOC-S01665657-1": "/job/Bengaluru/Supply-Chain-Operations-New-Associate_AIOC-S01665657-1",
    "ATCI-5385080-S2001241-1": "/job/Bengaluru/Program-Project-Management-Representativ_ATCI-5385080-S2001241-1"
}

base = "https://accenture.wd103.myworkdayjobs.com/wday/cxs/accenture/AccentureCareers"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

results = []
for jid, path in job_paths.items():
    url = base + path
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            info = data.get('jobPostingInfo', {})
            results.append({
                "req_id": jid,
                "api_req_id": info.get('jobReqId'),
                "title": info.get('title'),
                "posted": info.get('postedOn'),
                "location": info.get('location'),
                "status": "LIVE & VERIFIED",
                "link": f"https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers{path}"
            })
    except Exception as e:
        results.append({
            "req_id": jid,
            "status": f"ERROR: {e}",
            "link": ""
        })

print(f"Total checked: {len(results)}")
for r in results:
    print(f"[{r['status']}] {r['req_id']} -> {r.get('title')} | {r.get('posted')} | {r.get('location')}")

with open('linkedin_verified_job_ids.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
