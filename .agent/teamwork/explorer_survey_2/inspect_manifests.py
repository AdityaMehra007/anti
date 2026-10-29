import os, json

target_companies = [
    'accenture', 'deloitte', 'goldman', 'amazon', 'ibm',
    'jpmorgan', 'jp_morgan', 'kpmg', 'pwc',
    'walmart', 'delhivery', 'phonepe'
]

app_dir = 'applications_generated'
results = []

for item in sorted(os.listdir(app_dir)):
    full = os.path.join(app_dir, item)
    if not os.path.isdir(full):
        continue
    il = item.lower()
    for tc in target_companies:
        if tc in il:
            # check for manifest
            mf_path = os.path.join(full, 'APPLICATION_MANIFEST.json')
            if not os.path.exists(mf_path):
                mf_path = os.path.join(full, 'application_manifest.json')
            if os.path.exists(mf_path):
                with open(mf_path, 'r', encoding='utf-8') as f:
                    try:
                        mf = json.load(f)
                        results.append({
                            'folder': item,
                            'matched_company': tc,
                            'manifest': mf
                        })
                    except Exception as e:
                        print(f"Error reading {mf_path}: {e}")
            break

print(f"Total manifests matched: {len(results)}")
for r in results:
    mf = r['manifest']
    comp = mf.get('company_name') or mf.get('company')
    role = mf.get('target_role') or mf.get('role')
    corridor = mf.get('corridor_location') or mf.get('corridor')
    url = mf.get('careers_portal_url') or mf.get('portal_url')
    print(f"[{r['folder']}] {comp} | Role: {role} | Corridor: {corridor} | Portal: {url}")
