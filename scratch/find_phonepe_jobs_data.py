import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.phonepe.com/careers/job-openings/"
headers = {'User-Agent': 'Mozilla/5.0'}
with urllib.request.urlopen(urllib.request.Request(url, headers=headers), context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# look for scripts
scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
print("Scripts on PhonePe careers:")
for s in scripts:
    print(" ", s)

# check inline json or job arrays
job_data = re.findall(r'(\{"id":\s*["\']?[0-9]+["\']?,\s*"title":[^}]+\})', html)
print("Job data matches:", len(job_data))
for jd in job_data[:5]:
    print(" ", jd)

# check any greenhouse board or api URLs
apis = re.findall(r'https?://[^\s"\'<>]+(?:api|greenhouse|lever|workday|job)[^\s"\'<>]*', html)
print("APIs found:")
for a in set(apis):
    print(" ", a)
