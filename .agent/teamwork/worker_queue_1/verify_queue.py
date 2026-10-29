import csv
import json

with open('data/approval_queue.csv', 'r', encoding='utf-8') as f:
    csv_rows = list(csv.DictReader(f))

with open('data/approval_queue.json', 'r', encoding='utf-8') as f:
    json_rows = json.load(f)

print(f"CSV length: {len(csv_rows)}")
print(f"JSON length: {len(json_rows)}")
assert len(csv_rows) == len(json_rows) == 609, f"Mismatch: CSV {len(csv_rows)}, JSON {len(json_rows)}"

print("\nNewly staged rows (REF-0605 to REF-0609):")
for r in csv_rows[604:]:
    print("---")
    for k, v in r.items():
        val_str = str(v)
        if len(val_str) > 75:
            val_str = val_str[:75] + "..."
        print(f"  {k}: {val_str}")

# Parity check across all items
for idx, (cr, jr) in enumerate(zip(csv_rows, json_rows)):
    assert cr == jr, f"Discrepancy at row {idx}: {cr['Action ID']} vs {jr['Action ID']}"

print("\nFull Parity Check: 100% MATCH across all 609 rows!")
