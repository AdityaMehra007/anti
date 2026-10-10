import json

with open("scratch/cred_lever_jobs.json", encoding="utf-8") as f:
    jobs = json.load(f)

target_ids = ['b3fdba2a-802c-4e03-b445-5284c5e3c157', 'a65bef0e-0f4c-40af-b662-9313f255189e', '09022710-e79a-4cf0-8060-df0e1cd64263']

for j in jobs:
    jid = j.get("id")
    if jid in target_ids:
        print(f"=== [{jid}] {j.get('text')} ===")
        print("Team:", j.get("categories", {}).get("team"))
        print("Apply:", j.get("hostedUrl"))
        desc = j.get("descriptionPlain", "")
        lines = [l.strip() for l in desc.split('\n') if l.strip()]
        for l in lines[:15]:
            print("  ", l.encode('ascii', 'ignore').decode('ascii'))
        print()
