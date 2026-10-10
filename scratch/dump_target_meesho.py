import json

with open("scratch/meesho_bangalore_jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

target_ids = [
    '1de2fc88-e203-4f1a-8046-55df700de4be', # Trainee - Recruitment Coordinator
    '35a98774-fbca-4826-93a0-cc2b19bf2354', # Senior Associate / AM - Program Ops (Fulfilment & Experience)
    '3032374b-0010-4d19-8dd1-26c37c396cba', # AM Finance - Logistics Intelligence
    '1f2462b8-3548-466e-908f-dcae91cfaee1', # AM - Performance Marketing
    '538d386d-a584-41ed-91dc-607f83ca1c91', # DM - Logistics Intelligence
    '07d86780-64fb-4ecf-b1d1-9b4602b436de'  # DM - Revenue Intelligence and Governance
]

with open("scratch/meesho_target_roles_summary.txt", "w", encoding="utf-8") as out:
    for j in jobs:
        if j.get('id') in target_ids:
            out.write(f"\n=========================================\n")
            out.write(f"Title: {j.get('text')}\n")
            out.write(f"ID: {j.get('id')}\n")
            out.write(f"Team: {j.get('categories', {}).get('team')}\n")
            out.write(f"Department: {j.get('categories', {}).get('department')}\n")
            out.write(f"URL: {j.get('hostedUrl')}\n")
            desc = j.get('descriptionPlain', '')
            out.write(f"Description snippet:\n{desc[:600]}\n\n")
            for lst in j.get('lists', []):
                out.write(f"List: {lst.get('text')}\n")
                out.write(f"{lst.get('content')}\n")

print("Wrote summary to scratch/meesho_target_roles_summary.txt")
