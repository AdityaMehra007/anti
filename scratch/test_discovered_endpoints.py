import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

org_id = "4d757ba0-3d57-448a-b82c-238ed87ac90f"

endpoints = [
    f"https://api.turbohire.co/api/careerpage/details?orgId={org_id}",
    f"https://api.turbohire.co/api/careerpage?orgId={org_id}",
    f"https://api.turbohire.co/api/v3/jobs?orgId={org_id}",
    f"https://api.turbohire.co/job/publicjobs/{org_id}"
]

for ep in endpoints:
    req = urllib.request.Request(ep, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=6) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            print(f"SUCCESS {ep[:55]}... len: {len(content)}")
            print("Preview:", content[:200])
    except Exception as e:
        print(f"Failed {ep[:55]}...: {e}")
