import requests
import json
import re

url = "https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Workday jobs usually expose a direct API: /wday/talent/v1/jobs/... or wday/cxs/...
# Let's see what the page contains:
r = requests.get(url, headers=headers, timeout=10)
print("Status:", r.status_code)

# Try Workday CXS API:
# https://accenture.wd103.myworkdayjobs.com/wday/cxs/accenture/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1
api_url = "https://accenture.wd103.myworkdayjobs.com/wday/cxs/accenture/AccentureCareers/job/Bengaluru/Procurement-Operations-Associate_AIOC-S01664213-1"
r_api = requests.get(api_url, headers=headers, timeout=10)
print("API Status:", r_api.status_code)
if r_api.status_code == 200:
    data = r_api.json()
    job_info = data.get("jobPostingInfo", {})
    print("API Job Title:", job_info.get("title"))
    print("API Job Req ID:", job_info.get("jobReqId"))
    print("API Job Description snippet:\n", job_info.get("jobDescription", "")[:800])
    with open("e:/anti/scraped_accenture_jd.json", "w", encoding="utf-8") as f:
        json.dump(job_info, f, indent=2)
else:
    print("API response:", r_api.text[:300])
