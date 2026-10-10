import urllib.request
import json
import time

url = 'https://jobs.api.mercedes-benz.com/search'

all_jobs = []
first_item = 1
items_per_page = 100

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

while True:
    payload = {
        'LanguageCode': 'EN',
        'SearchParameters': {
            'FirstItem': first_item,
            'CountItem': items_per_page,
            'Sort': [{'Criterion': 'PublicationStartDate', 'Direction': 'DESC'}]
        },
        'SearchCriteria': [
            {'CriterionName': 'ParentOrganization', 'CriterionValue': [140]},
            {'CriterionName': 'PositionLocation.Country', 'CriterionValue': [390]}
        ]
    }
    
    print(f"Fetching from {first_item}...")
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('SearchResult', {}).get('SearchResultItems', [])
            total = data.get('SearchResult', {}).get('SearchResultCountAll', 0)
            print(f"  Got {len(items)} items. Total available: {total}")
            for it in items:
                all_jobs.append(it.get('MatchedObjectDescriptor', {}))
            if len(all_jobs) >= total or len(items) == 0:
                break
            first_item += len(items)
    except Exception as e:
        print(f"Error at {first_item}: {e}")
        break
    time.sleep(0.3)

with open('scratch/mbrdi_all_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(all_jobs, f, indent=2, ensure_ascii=False)

print(f"Total MBRDI jobs saved: {len(all_jobs)} to scratch/mbrdi_all_jobs.json")
