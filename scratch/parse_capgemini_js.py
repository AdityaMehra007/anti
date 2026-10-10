import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
url = 'https://www.capgemini.com/in-en/wp-content/plugins/cg-jobs/inc/search/app/build/cg-jobs-search-frontend.build.js?ver=1.0.569'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    js_text = resp.read().decode('utf-8')
    print('JS Length:', len(js_text))
    matches = re.findall(r'wp-json[a-zA-Z0-9_\-\/\.]*', js_text)
    print('Matches with wp-json:', set(matches))
    api_calls = re.findall(r'/api/[a-zA-Z0-9_\-\/\.]*', js_text)
    print('Matches with /api/:', set(api_calls))
    fetch_calls = re.findall(r'fetch\([^\)]+\)', js_text)
    print('Fetch calls count:', len(fetch_calls))
    for fc in fetch_calls[:5]:
        print('Fetch snippet:', fc[:120])
