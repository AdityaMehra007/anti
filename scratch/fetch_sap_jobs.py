import urllib.request
import re
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

queries = ['operations', 'finance', 'commercial', 'associate', 'consultant', 'sales', 'business', 'early talent', 'specialist']
results = []
seen = set()

for q in queries:
    encoded_q = urllib.parse.quote(q)
    url = f"https://careers.sap.com/search/?q={encoded_q}&locationsearch=Bangalore&optionsFacetsDD_country=IN"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'href="/job/([^/]+)/([0-9]+)/"', html)
            for raw_slug, jid in matches:
                if jid not in seen:
                    seen.add(jid)
                    title = urllib.parse.unquote(raw_slug).replace('-', ' ')
                    results.append({
                        "job_id": jid,
                        "title": title,
                        "query": q,
                        "link": f"https://careers.sap.com/job/{raw_slug}/{jid}/"
                    })
    except Exception as e:
        print(f"Error querying {q}: {e}")

print(f"Total unique roles found: {len(results)}")
with open("scratch/sap_bangalore_roles.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

for r in results[:20]:
    print(f"[{r['job_id']}] {r['title']}")
