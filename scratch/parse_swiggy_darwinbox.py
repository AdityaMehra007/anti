import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://swiggy.darwinbox.in/jobs"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

with urllib.request.urlopen(urllib.request.Request(url, headers=headers), context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

print(f"HTML len: {len(html)}")

# look for job listings in darwinbox HTML
job_cards = re.findall(r'<div[^>]*class="[^"]*job-card[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
print("Job cards:", len(job_cards))

# look for job titles or links
job_links = re.findall(r'href="([^"]*/jobs/view/[^"]*|[^"]*/ms/candidate/[^"]*)"', html)
print("Job links:", len(job_links))
for l in set(job_links[:10]):
    print(" ", l)

# look for JSON embedded in darwinbox HTML
embedded_json = re.findall(r'var\s+jobs_data\s*=\s*({.*?});', html, re.DOTALL)
if not embedded_json:
    embedded_json = re.findall(r'var\s+all_jobs\s*=\s*(\[.*?\]);', html, re.DOTALL)

if embedded_json:
    print("Found embedded jobs JSON!")
    try:
        jd = json.loads(embedded_json[0])
        print("Embedded jobs count:", len(jd))
    except Exception as e:
        print("JSON parse error:", e)
else:
    # search for titles
    titles = re.findall(r'class="[^"]*job-title[^"]*"[^>]*>([^<]+)<', html)
    print("Job titles found via class:", len(titles))
    for t in titles[:10]:
        print(" ", t.strip())
