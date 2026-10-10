import glob
import os
import csv

id_patterns = ['id', 'job_id', 'job id', 'req_id', 'requisition_id', 'reference_id', 'ref_code', 'target id', 'display_id']

csvs = glob.glob('*.csv')
results = {}
total_explicit_job_ids = 0

for c in sorted(csvs):
    with open(c, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            continue
        matching_cols = []
        for idx, col_name in enumerate(header):
            cleaned = col_name.strip().lower().replace('\ufeff', '')
            if any(cleaned == p or cleaned.endswith('_id') or cleaned.endswith(' id') or 'req_id' in cleaned or 'ref_code' in cleaned or 'reference_id' in cleaned for p in id_patterns):
                matching_cols.append((idx, col_name))
        
        if matching_cols:
            rows = list(reader)
            col_idx = matching_cols[0][0]
            valid_ids = [r[col_idx] for r in rows if len(r) > col_idx and r[col_idx].strip()]
            results[c] = (matching_cols[0][1], len(valid_ids), valid_ids[:3])
            total_explicit_job_ids += len(valid_ids)

print("--- EXPLICIT JOB ID & REQUISITION ID LEDGERS ---")
for fn, (col, cnt, samples) in results.items():
    cleaned_col = col.replace('\ufeff', '')
    print(f"{fn} | Column: '{cleaned_col}' | IDs: {cnt} | Samples: {samples}")

print(f"\nTOTAL EXPLICIT ID RECORDS FOUND: {total_explicit_job_ids}")
