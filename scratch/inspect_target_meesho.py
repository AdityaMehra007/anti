import json

with open("scratch/meesho_bangalore_jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

for j in jobs:
    dept = j.get('categories', {}).get('department', '')
    if dept in ['Commerce Platform', 'CEO Office', 'AI Services']:
        print(f"[{dept}] {j.get('id')} - {j.get('text')} - {j.get('hostedUrl')}")

# Let's inspect the details of the Trainee and Associate roles
target_ids = ['1de2fc88-e203-4f1a-8046-55df700de4be', '35a98774-fbca-4826-93a0-cc2b19bf2354', '3032374b-0010-4d19-8dd1-26c37c396cba', '1690adaa-ec47-4246-a40e-995b859545f2']
print("\n--- TARGET ROLES DETAILS ---")
for j in jobs:
    if j.get('id') in target_ids:
        print(f"\nTitle: {j.get('text')}")
        print(f"URL: {j.get('hostedUrl')}")
        desc = j.get('descriptionPlain', '')
        print("Description snippet:", desc[:500] if desc else "No plain desc")
        lists = j.get('lists', [])
        for l in lists:
            print(f"List ({l.get('text')}):")
            for item in l.get('content', '').split('</li>')[:5]:
                print("  *", item.replace('<li>', '').strip())
