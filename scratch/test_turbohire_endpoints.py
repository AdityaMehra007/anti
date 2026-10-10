import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

org_id = "4d757ba0-3d57-448a-b82c-238ed87ac90f"

test_urls = [
    f"https://api.turbohire.co/api/careerpage/jobs?orgId={org_id}",
    f"https://api.turbohire.co/api/careerpage/getjobs?orgId={org_id}",
    f"https://api.turbohire.co/api/career/jobs?orgId={org_id}",
    f"https://api.turbohire.co/api/jobs/public?orgId={org_id}",
    f"https://api.turbohire.co/api/careerpage/{org_id}/jobs",
    f"https://flipkart.turbohire.co/api/careerpage/jobs?orgId={org_id}"
]

for u in test_urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            print(f"SUCCESS {u[:45]}... len: {len(content)}")
            print("Preview:", content[:150])
            break
    except Exception as e:
        print(f"Failed {u[:45]}...: {e}")
