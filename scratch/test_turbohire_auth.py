import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

org_id = "4d757ba0-3d57-448a-b82c-238ed87ac90f"

url = "https://api.turbohire.co/api/token/noauth"
payload = {"orgId": org_id}
data = json.dumps(payload).encode('utf-8')
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json'
}

req = urllib.request.Request(url, data=data, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=6) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print("Success noauth token!")
        print("Keys:", list(res.keys()) if isinstance(res, dict) else res)
        token = res.get("token") or res.get("access_token")
        print("Token preview:", str(token)[:50])
        
        # Now call /api/v3/jobs with token
        if token:
            job_url = f"https://api.turbohire.co/api/v3/jobs?orgId={org_id}"
            job_req = urllib.request.Request(job_url, headers={
                'Authorization': f'Bearer {token}',
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json'
            })
            with urllib.request.urlopen(job_req, context=ctx, timeout=6) as job_resp:
                job_res = json.loads(job_resp.read().decode('utf-8'))
                print("Jobs result keys:", list(job_res.keys()) if isinstance(job_res, dict) else len(job_res))
                with open("scratch/turbohire_flipkart_jobs.json", "w", encoding="utf-8") as f:
                    json.dump(job_res, f, indent=2)
except Exception as e:
    print(f"Error: {e}")
