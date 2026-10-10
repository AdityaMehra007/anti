import urllib.request
import json
import re

# Test searching for India / Bangalore
queries = [
    'https://careers.astrazeneca.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&SortCriteria=0&OrgIds=7684&PostalCode=&Keywords=&Location=India',
    'https://careers.astrazeneca.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&SortCriteria=0&OrgIds=7684&PostalCode=&Keywords=&Location=Bengaluru',
    'https://careers.astrazeneca.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&SortCriteria=0&OrgIds=7684&PostalCode=&Keywords=&Location=Bangalore',
    'https://careers.astrazeneca.com/search-jobs/India/7684/2',
    'https://careers.astrazeneca.com/search-jobs/Bengaluru/7684/4'
]

for q in queries:
    print(f"Testing {q}...")
    try:
        req = urllib.request.Request(q, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Accept': 'application/json, text/html, */*',
            'X-Requested-With': 'XMLHttpRequest'
        })
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            print(f"  Status: {resp.status}, length: {len(content)}")
            # check if json
            try:
                data = json.loads(content)
                print(f"  JSON! keys: {list(data.keys())}, totalMatches: {data.get('totalMatches')}, hasJobs: {data.get('hasJobs')}")
                if 'results' in data:
                    print(f"  results length: {len(data['results'])}")
                    # count jobs
                    job_links = re.findall(r'href=\"/job/[^\"]+\"', data['results'])
                    print(f"  job links in results: {len(job_links)}")
            except Exception:
                # check html
                matches = re.findall(r'\d+\s*Jobs?', content, re.I)
                print(f"  HTML matches for Jobs: {matches[:3]}")
    except Exception as e:
        print(f"  Error: {e}")
