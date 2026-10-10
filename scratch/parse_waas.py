import urllib.request
import json
import csv

def query_yc_bengaluru():
    app_id = '45BWZJ1SGC'
    api_key = 'ODFmNDlkZTc2MjQ5MjQwMGIxMmNmYWY2YTFkZDdhMjg0M2VjODEzN2VjODY1MWM5NTJiN2E3ZDgzOTBlYzU4MWFuYWx5dGljc1RhZ3M9d2FhcyZyZXN0cmljdEluZGljZXM9JTJBX3Byb2R1Y3Rpb24mdGFnRmlsdGVycz0lNUIlNUIlMjJub25lJTIyJTVEJTVEJnZhbGlkVW50aWw9MTc5MTY3MzkzNQ=='
    url = f'https://{app_id}-dsn.algolia.net/1/indexes/*/queries'

    # Try query with query='Bengaluru' or facets
    queries = [
        {
            'indexName': 'Job_production',
            'params': 'query=Bengaluru&hitsPerPage=100'
        },
        {
            'indexName': 'Job_production',
            'params': 'query=Bangalore&hitsPerPage=100'
        }
    ]

    payload = {'requests': queries}

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'X-Algolia-Application-Id': app_id,
            'X-Algolia-API-Key': api_key,
            'Content-Type': 'application/json'
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Failed to query Algolia: {e}")
        return

    seen_ids = set()
    bengaluru_jobs = []

    for result in data.get('results', []):
        hits = result.get('hits', [])
        print(f"Index returned {len(hits)} hits.")
        for h in hits:
            job_id = h.get('objectID') or str(h.get('id', ''))
            if not job_id or job_id in seen_ids:
                continue
                
            title = h.get('title', '')
            company = h.get('company_name', '')
            slug = h.get('company_slug', '')
            batch = h.get('batch', '')
            locations = h.get('locations', [])
            loc_str = ", ".join(locations) if isinstance(locations, list) else str(locations)
            
            # Filter strictly for Bangalore / Bengaluru or Remote in India
            if any(term in loc_str.lower() for term in ['bengaluru', 'bangalore', 'india']):
                seen_ids.add(job_id)
                
                # Check salary / equity
                min_sal = h.get('min_salary')
                max_sal = h.get('max_salary')
                equity = h.get('equity_string') or h.get('equity') or ''
                sal_str = ""
                if min_sal and max_sal:
                    sal_str = f"${min_sal:,} - ${max_sal:,}"
                elif min_sal:
                    sal_str = f"${min_sal:,}+"
                    
                apply_url = f"https://www.workatastartup.com/jobs/{job_id}"
                company_url = f"https://www.workatastartup.com/companies/{slug}" if slug else ""
                
                bengaluru_jobs.append({
                    'Job Title': title,
                    'Company': company,
                    'YC Batch': batch,
                    'Locations': loc_str,
                    'Compensation': sal_str,
                    'Equity': equity,
                    'Job ID': job_id,
                    'Company URL': company_url,
                    'Apply URL': apply_url
                })

    print(f"\nTotal verified YC startups hiring in Bengaluru: {len(bengaluru_jobs)}")
    for j in bengaluru_jobs[:10]:
        print(f"- {j['Job Title']} at {j['Company']} ({j['YC Batch']})")
        print(f"  Location: {j['Locations']} | Comp: {j['Compensation']} | Equity: {j['Equity']}")
        print(f"  URL: {j['Apply URL']}")

    with open('yc_workatastartup_bengaluru_jobs.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Job Title', 'Company', 'YC Batch', 'Locations', 'Compensation', 'Equity', 'Job ID', 'Company URL', 'Apply URL']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(bengaluru_jobs)

    print("Saved to yc_workatastartup_bengaluru_jobs.csv successfully.")

if __name__ == '__main__':
    query_yc_bengaluru()
