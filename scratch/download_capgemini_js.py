import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
url = 'https://www.capgemini.com/in-en/wp-content/plugins/cg-jobs/inc/search/app/build/cg-jobs-search-frontend.build.js?ver=1.0.569'

headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    js_text = resp.read().decode('utf-8')
    with open('scratch/capgemini_app.js', 'w', encoding='utf-8') as f:
        f.write(js_text)

idx = js_text.find('cg_jobs_jobstream_url')
while idx != -1:
    print('Found around cg_jobs_jobstream_url:')
    print(js_text[max(0, idx-50):min(len(js_text), idx+200)])
    print('='*50)
    idx = js_text.find('cg_jobs_jobstream_url', idx+1)
