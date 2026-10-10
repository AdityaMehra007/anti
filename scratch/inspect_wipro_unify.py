import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
url = 'https://careers.wipro.com/platform/js/j2w/min/j2w.searchResultsUnify.min.js?h=275f70e9'
headers = {'User-Agent': 'Mozilla/5.0'}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    js = resp.read().decode('utf-8')
    with open('scratch/wipro_searchResultsUnify.js', 'w', encoding='utf-8') as f:
        f.write(js)

print('Saved scratch/wipro_searchResultsUnify.js, length:', len(js))
urls = set(re.findall(r'/[a-zA-Z0-9_\-\.\/]+', js))
for u in urls:
    if any(k in u.lower() for k in ['search', 'job', 'service', 'api']):
        print('Matching URL path:', u)
