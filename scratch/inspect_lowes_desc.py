import urllib.request
import re

url = "https://talent.lowes.com/in/en/job/JR-02672638"
headers = {'User-Agent': 'Mozilla/5.0'}
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print("Page length:", len(html))
        # look for job description
        desc_match = re.search(r'<div class="jd-info">(.*?)</div>\s*<div class="ats-description"', html, re.S)
        if not desc_match:
            desc_match = re.search(r'<section class="job-description">(.*?)</section>', html, re.S)
        if desc_match:
            print("Found description!")
            print(re.sub(r'<[^>]+>', ' ', desc_match.group(1))[:1500])
        else:
            # find text between "What You Will Do" or "Roles and Responsibilities"
            text = re.sub(r'<[^>]+>', ' ', html)
            pos = text.find("Marketplace Management")
            if pos != -1:
                print(text[pos:pos+1500])
except Exception as e:
    print("Error:", e)
