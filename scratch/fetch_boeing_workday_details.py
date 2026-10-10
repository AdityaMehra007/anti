import urllib.request
import json
import time

with open('scratch/boeing_workday_india_jobs.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

# Keep only the 8 India jobs
india_jobs = [j for j in jobs if 'India' in j.get('locationsText', '')]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Accept': 'application/json'
}

detailed_records = []
for j in india_jobs:
    path = j.get('externalPath')
    title = j.get('title')
    req = j.get('bulletFields', [''])[0]
    loc = j.get('locationsText')
    detail_url = f"https://boeing.wd1.myworkdayjobs.com/wday/cxs/boeing/EXTERNAL_CAREERS{path}"
    safe_title = title.encode('ascii', 'ignore').decode('ascii')
    print(f"Fetching {safe_title} ({req})...")
    try:
        req_obj = urllib.request.Request(detail_url, headers=headers)
        with urllib.request.urlopen(req_obj) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            info = data.get('jobPostingInfo', {})
            detailed_records.append({
                'title': info.get('title'),
                'jobReqId': info.get('jobReqId'),
                'location': info.get('location'),
                'timeType': info.get('timeType'),
                'postedOn': info.get('postedOn'),
                'externalPath': path,
                'workdayUrl': f"https://boeing.wd1.myworkdayjobs.com/EXTERNAL_CAREERS{path}",
                'radancyUrl': f"https://jobs.boeing.com/job/... (via jobs.boeing.com)",
                'jobDescription': info.get('jobDescription', '')
            })
    except Exception as e:
        print(f"Error fetching {detail_url}: {e}")
    time.sleep(0.3)

with open('scratch/boeing_workday_india_details.json', 'w', encoding='utf-8') as f:
    json.dump(detailed_records, f, indent=2, ensure_ascii=False)

print(f"Successfully saved {len(detailed_records)} India jobs to scratch/boeing_workday_india_details.json!")
