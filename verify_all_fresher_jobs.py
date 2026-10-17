import json
import urllib.request
import time

def main():
    with open('categorized_mega_bengaluru_jobs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_assoc_jobs = []
    for cat, jobs in data.items():
        for j in jobs:
            t = j['title'].lower()
            if 'new associate' in t or 'representative' in t:
                new_assoc_jobs.append({
                    'category': cat,
                    'title': j['title'],
                    'req_id': j['req_id'],
                    'posted': j['posted'],
                    'path': j['path'],
                    'link': j['link']
                })
    
    print(f"Total Level 13 (New Associate / Representative) jobs: {len(new_assoc_jobs)}")
    
    # Save to a clean json file
    with open('verified_fresher_accenture_jobs.json', 'w', encoding='utf-8') as out_f:
        json.dump(new_assoc_jobs, out_f, indent=2)

    # Print grouped by Category
    by_cat = {}
    for job in new_assoc_jobs:
        by_cat.setdefault(job['category'], []).append(job)

    for cat, jobs in by_cat.items():
        print(f"\n==========================================")
        print(f"CATEGORY: {cat} ({len(jobs)} openings)")
        print(f"==========================================")
        for j in jobs:
            print(f"  • {j['title']}")
            print(f"    Job ID : {j['req_id']}")
            print(f"    Posted : {j['posted']}")
            print(f"    Link   : {j['link']}")

if __name__ == '__main__':
    main()
