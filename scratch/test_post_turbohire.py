import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

org_id = "4d757ba0-3d57-448a-b82c-238ed87ac90f"

endpoints = [
    ("https://api.turbohire.co/api/careerpage", {"orgId": org_id}),
    ("https://api.turbohire.co/api/v3/jobs", {"orgId": org_id}),
    ("https://api.turbohire.co/api/jobs/all", {"orgId": org_id}),
    ("https://api.turbohire.co/api/careerpage/getjobs", {"orgId": org_id})
]

for ep, payload in endpoints:
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(ep, data=data, headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=6) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            print(f"SUCCESS POST {ep[:45]}... len: {len(content)}")
            print("Preview:", content[:300])
            try:
                parsed = json.loads(content)
                if isinstance(parsed, list):
                    print(f"Returned list of {len(parsed)} items!")
                elif isinstance(parsed, dict):
                    print(f"Keys: {list(parsed.keys())}")
            except:
                pass
    except Exception as e:
        print(f"Failed POST {ep[:45]}...: {e}")
