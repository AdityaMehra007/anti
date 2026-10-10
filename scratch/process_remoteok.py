import json
import csv
import re

def process_remoteok():
    with open('scratch/remoteok_api.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    jobs = data[1:] if isinstance(data, list) else []
    print(f"Total live jobs in RemoteOK API: {len(jobs)}")

    # We want jobs accessible to engineers/leaders in Bengaluru, India
    # 1. Explicitly mentioning India / Bengaluru / Bangalore in location or description
    # 2. Worldwide / Global remote roles (open to talent in India / APAC timezones)
    
    india_specific = []
    worldwide_open = []

    for j in jobs:
        pos = j.get('position', '').strip()
        comp = j.get('company', '').strip()
        loc = j.get('location', '').strip()
        tags = j.get('tags', [])
        tag_str = ", ".join(tags)
        url = j.get('url', '')
        date = j.get('date', '')[:10]
        
        sal_min = j.get('salary_min')
        sal_max = j.get('salary_max')
        comp_str = ""
        if sal_min and sal_max and (sal_min > 0 or sal_max > 0):
            comp_str = f"${sal_min:,} - ${sal_max:,} USD"
        elif sal_min and sal_min > 0:
            comp_str = f"${sal_min:,}+ USD"
            
        desc = j.get('description', '').lower()
        loc_lower = loc.lower()

        record = {
            'Job Title': pos,
            'Company': comp,
            'Eligible Location': loc if loc else 'Worldwide / Any Location',
            'Compensation': comp_str if comp_str else 'Competitive / Equity',
            'Tags / Skills': tag_str,
            'Posted Date': date,
            'Apply URL': url
        }

        if any(term in loc_lower for term in ['india', 'bangalore', 'bengaluru']) or 'bangalore' in desc or 'bengaluru' in desc:
            record['Geographic Scope'] = 'India / Bengaluru Dedicated'
            india_specific.append(record)
        elif any(term in loc_lower for term in ['worldwide', 'global', 'anywhere']) or loc == '' or 'remote' in loc_lower:
            record['Geographic Scope'] = 'Worldwide Remote (India Eligible)'
            worldwide_open.append(record)

    print(f"India / Bengaluru Dedicated Requisitions: {len(india_specific)}")
    print(f"Worldwide Remote Roles Open to Bengaluru Talent: {len(worldwide_open)}")

    combined = india_specific + worldwide_open
    print(f"Total Exporting: {len(combined)} roles")

    # Export to CSV
    with open('remoteok_bengaluru_global_jobs.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Job Title', 'Company', 'Geographic Scope', 'Eligible Location', 'Compensation', 'Tags / Skills', 'Posted Date', 'Apply URL']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined)

    print("Saved to remoteok_bengaluru_global_jobs.csv successfully.")

    # Show highlights
    print("\nSample India-Dedicated Roles:")
    for r in india_specific[:5]:
        print(f"- {r['Job Title']} at {r['Company']} | Comp: {r['Compensation']} | URL: {r['Apply URL']}")

    print("\nSample Worldwide Global Roles:")
    for r in worldwide_open[:5]:
        print(f"- {r['Job Title']} at {r['Company']} | Loc: {r['Eligible Location']} | Comp: {r['Compensation']} | URL: {r['Apply URL']}")

if __name__ == '__main__':
    process_remoteok()
