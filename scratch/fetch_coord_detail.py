import urllib.request
import json

url = "https://walmart.wd504.myworkdayjobs.com/wday/cxs/walmart/WalmartExternal/job/IN-KA-BANGALORE-Home-Office-CUMULUS/RESOLUTION-COORDINATOR--CONTACT-CENTER_R-2387318"
headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    job = data.get('jobPostingInfo', {})
    
with open("scratch/walmart_resolution_coord.json", "w", encoding="utf-8") as out:
    json.dump(job, out, indent=2)

desc = job.get('jobDescription', '')
with open("scratch/walmart_resolution_coord_desc.txt", "w", encoding="utf-8") as out:
    out.write(f"Title: {job.get('title')}\n")
    out.write(f"Job Req ID: {job.get('jobReqId')}\n")
    out.write(f"Location: {job.get('location')}\n")
    out.write(f"\n{desc}\n")

print("Saved description successfully!")
