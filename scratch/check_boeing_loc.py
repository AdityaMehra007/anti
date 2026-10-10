import urllib.request
import json

url = 'https://boeing.wd1.myworkdayjobs.com/wday/cxs/boeing/EXTERNAL_CAREERS/jobs'
payload = {
    'appliedFacets': {},
    'limit': 20,
    'offset': 0,
    'searchText': ''
}
req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    for f in data.get('facets', []):
        if f.get('facetParameter') == 'locationMainGroup':
            print("locationMainGroup values:")
            for v in f.get('values', []):
                print(f"  - {v.get('descriptor')} ({v.get('count')}) [id: {v.get('id')}]")
