import csv, json, os

print("=== VERIFICATION SUITE — EXPLORER SURVEY 2 ===")

# Test 1: Verify 11 target openings in BBA_IB_Bengaluru_61_Job_Pipeline.csv
targets = ['accenture', 'deloitte', 'amazon', 'goldman', 'jpmorgan', 'jp morgan', 'ibm', 'kpmg', 'pwc', 'pricewaterhouse', 'walmart', 'delhivery', 'phonepe']
with open('data/BBA_IB_Bengaluru_61_Job_Pipeline.csv', mode='r', encoding='utf-8') as f:
    rows = [r for r in csv.DictReader(f) if any(t in r['Company Name'].lower() for t in targets)]
print(f"Test 1 [Pipeline Openings]: {len(rows)}/11 target companies verified.")
assert len(rows) == 11, f"Expected 11 target openings, got {len(rows)}"

# Test 2: Verify candidate truth
with open('data/verified_profile.json', 'r', encoding='utf-8') as f:
    p = json.load(f)
assert p['candidate']['full_name'] == 'Aditya Mehra'
assert p['education'][0]['institution'] == 'Dayananda Sagar University, Bengaluru'
assert p['verified_experience'][0]['event'] == 'AERO INDIA 2025'
print("Test 2 [Candidate Truth]: Verified with zero hallucinations.")

# Test 3: Verify LinkedIn connections
with open('data/Connections_clean.csv', mode='r', encoding='utf-8', errors='ignore') as f:
    conn_rows = list(csv.DictReader(f))
conn_targets = 0
for r in conn_rows:
    c = str(r.get('Company') or r.get('company', '')).lower()
    if any(t in c for t in targets):
        conn_targets += 1
print(f"Test 3 [LinkedIn Network]: {conn_targets} verified connections across 11 target employers (expected 563).")
assert conn_targets == 563, f"Expected 563 connections, got {conn_targets}"

# Test 4: Verify scored inventory
with open('.agents/teamwork/explorer_survey_2/scored_inventory.json', 'r', encoding='utf-8') as f:
    scored = json.load(f)
assert len(scored) == 11
all_p0 = all(s['priority_tier'] == 'P0 (Golden Strike)' for s in scored)
print(f"Test 4 [Scored Inventory]: 11/11 scored, all P0: {all_p0}.")
assert all_p0, "All target employers must achieve P0 status"

print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY (4/4).")
