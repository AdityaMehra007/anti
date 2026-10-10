import urllib.request
import json

url = "https://walmart.wd504.myworkdayjobs.com/wday/cxs/walmart/WalmartExternal/job/IN-KA-BANGALORE-Home-Office-CUMULUS/RESOLUTION-COORDINATOR--CONTACT-CENTER_R-2387318"
headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        job = data.get('jobPostingInfo', {})
        print("Title:", job.get('title'))
        print("Job Req ID:", job.get('jobReqId'))
        print("Location:", job.get('location'))
        print("Time Type:", job.get('timeType'))
        print("Start date:", job.get('startDate'))
        desc = job.get('jobDescription', '')
        print("\nJob Description:")
        print(desc[:1500])
        with open("scratch/walmart_resolution_coord.json", "w", encoding="utf-8") as out:
            json.dump(job, out, indent=2)
except Exception as e:
    print("Error:", e)
