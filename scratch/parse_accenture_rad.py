import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
url = 'https://www.accenture.com/etc.clientlibs/cio-sites/clientlibs/clientlib-rad.lc-0ce37e59b0730e08c6779bf56351a115-lc.min.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    js = resp.read().decode('utf-8')
    print('JS Length:', len(js))
    with open('scratch/accenture_rad.js', 'w', encoding='utf-8') as f:
        f.write(js)

# Find search URLs or API endpoints
matches = re.findall(r'/api/[a-zA-Z0-9_\-\/\.]*', js)
print('Matches with /api/:', set(matches[:20]))

solr_matches = re.findall(r'https?://[a-zA-Z0-9_\-\.]+(?:search|solr|api)[a-zA-Z0-9_\-\/\.\?=&]*', js)
print('Solr / Search URLs:', set(solr_matches[:20]))

keywords = [m for m in re.findall(r'[a-zA-Z0-9_\-]+Endpoint', js)]
print('Endpoints named:', set(keywords))
