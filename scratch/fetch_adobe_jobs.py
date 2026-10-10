import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://careers.adobe.com/us/en/search-results?qcity=Bangalore&qstate=Karn%C4%81taka&qcountry=India"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# check phApp
ph_matches = re.findall(r'phApp\.[a-zA-Z0-9_.]+', html)
print("phApp references:", set(ph_matches))

# look for ddo (digital data object) or eVar or pageData
ddo = re.findall(r'phApp\.ddo\s*=\s*({.*?});', html, re.DOTALL)
if ddo:
    print("Found ddo!")
    try:
        ddo_json = json.loads(ddo[0])
        print("ddo keys:", list(ddo_json.keys()))
        if "jobData" in ddo_json:
            print("jobData keys:", list(ddo_json["jobData"].keys()))
        if "searchResult" in ddo_json:
            print("searchResult keys:", list(ddo_json["searchResult"].keys()))
            jobs = ddo_json["searchResult"].get("jobs", [])
            print(f"Jobs count: {len(jobs)}")
            for j in jobs[:5]:
                print(j.get("jobId"), j.get("title"), j.get("city"))
    except Exception as e:
        print("Error parsing ddo:", e)

# Phenom widgets API
# Usually POST to https://careers.adobe.com/widgets with refNum or search params
widgets = re.findall(r'/widgets[^"\']*', html)
print("Widgets endpoints:", set(widgets))
