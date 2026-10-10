import urllib.request
import json

url = 'https://shell.wd3.myworkdayjobs.com/wday/cxs/shell/shellcareers/jobs'
payload = {
    'appliedFacets': {
        'locationCountry': ['c4f78be1a8f14da0ab49ce1162348a5e']
    },
    'limit': 20,
    'offset': 0,
    'searchText': ''
}
req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    for f in data.get('facets', []):
        if 'location' in f.get('facetParameter', '').lower():
            print(f"Facet: {f.get('facetParameter')}")
            for v in f.get('values', []):
                print(f"  {v.get('descriptor')} -> {v.get('count')}")
