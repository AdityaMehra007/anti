import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Cutshort details
try:
    html = urllib.request.urlopen(urllib.request.Request('https://cutshort.io/jobs/startup-jobs-in-bangalore-bengaluru', headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    if m:
        d = json.loads(m.group(1))
        queries = d.get('props', {}).get('pageProps', {}).get('dehydratedState', {}).get('queries', [])
        for i, q in enumerate(queries):
            query_key = q.get('queryKey', [])
            print(f"Query {i} key: {query_key}")
            state_data = q.get('state', {}).get('data', {})
            if isinstance(state_data, dict):
                inner_data = state_data.get('data', {})
                if isinstance(inner_data, dict):
                    print(f"   inner_data keys: {list(inner_data.keys())}")
                    job_list = inner_data.get('jobs', [])
                    print(f"   job_list length: {len(job_list)}")
                    if job_list:
                        sample = job_list[0]
                        print("   Sample job keys:", list(sample.keys()))
                        print("   Sample title:", sample.get('title'))
                        print("   Sample company:", sample.get('companyName'))
                        print("   Sample salary:", sample.get('salary'))
                        print("   Sample location:", sample.get('location'))
                        print("   Sample slug / link:", sample.get('slug'))
except Exception as e:
    print("Cutshort error:", e)

# Hirist details
try:
    html = urllib.request.urlopen(urllib.request.Request('https://www.hirist.tech/product-jobs?source=homepage', headers=headers), timeout=10).read().decode('utf-8', errors='ignore')
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    if m:
        d = json.loads(m.group(1))
        initialState = d.get('props', {}).get('pageProps', {}).get('initialState', {})
        job_state = initialState.get('job', {})
        print("Hirist job_state keys:", list(job_state.keys()))
        job_list = job_state.get('jobs', []) or job_state.get('jobList', [])
        print(f"Hirist jobList length: {len(job_list)}")
        if job_list:
            sample = job_list[0]
            print("Hirist sample job keys:", list(sample.keys()) if isinstance(sample, dict) else sample)
            if isinstance(sample, dict):
                print("Hirist sample title:", sample.get('title'))
                print("Hirist sample company:", sample.get('company'))
                print("Hirist sample loc:", sample.get('locations'))
                print("Hirist sample exp:", sample.get('minExp'), "-", sample.get('maxExp'))
except Exception as e:
    print("Hirist error:", e)
