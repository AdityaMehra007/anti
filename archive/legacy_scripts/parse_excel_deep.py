"""
Deep parser for BBA_International_Business_1400_Companies.xlsx & BBA_International_Business_Bangalore_Job_Pipeline.xlsx
Extracts exact sheets, headers, sample rows, and summary stats.
"""

import os
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

WORKSPACE = Path(r"e:\anti")
FILE_1400 = WORKSPACE / "BBA_International_Business_1400_Companies.xlsx"
FILE_PIPELINE = WORKSPACE / "BBA_International_Business_Bangalore_Job_Pipeline.xlsx"

def parse_xlsx(file_path):
    print(f"\n==================================================")
    print(f"DEEP PARSING: {file_path.name}")
    print(f"==================================================")
    
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return
        
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            # Shared strings
            shared_strings = []
            if 'xl/sharedStrings.xml' in z.namelist():
                ss_content = z.read('xl/sharedStrings.xml')
                ss_root = ET.fromstring(ss_content)
                for elem in ss_root.findall('.//{*}t'):
                    shared_strings.append(elem.text or "")
                    
            print(f"Shared strings loaded: {len(shared_strings)}")
            
            # List sheets
            sheets = [f for f in z.namelist() if f.startswith('xl/worksheets/sheet')]
            print(f"Sheets found: {len(sheets)}")
            
            for sheet_name in sheets:
                print(f"\n--- Sheet: {sheet_name} ---")
                sheet_content = z.read(sheet_name)
                sheet_root = ET.fromstring(sheet_content)
                
                rows = []
                for row_elem in sheet_root.findall('.//{*}row'):
                    row_vals = []
                    for cell in row_elem.findall('.//{*}c'):
                        val_type = cell.attrib.get('t', '')
                        val_elem = cell.find('{*}v')
                        if val_elem is not None:
                            val = val_elem.text
                            if val_type == 's' and val and val.isdigit():
                                idx = int(val)
                                row_vals.append(shared_strings[idx] if idx < len(shared_strings) else val)
                            else:
                                row_vals.append(val or "")
                        else:
                            is_elem = cell.find('.//{*}t')
                            if is_elem is not None:
                                row_vals.append(is_elem.text or "")
                            else:
                                row_vals.append("")
                    if any(row_vals):
                        rows.append(row_vals)
                        
                print(f"Total rows extracted: {len(rows)}")
                if rows:
                    print("Header row:", rows[0])
                    print("Sample Data Row 1:", rows[1] if len(rows) > 1 else "N/A")
                    print("Sample Data Row 2:", rows[2] if len(rows) > 2 else "N/A")
                    print("Sample Data Row 3:", rows[3] if len(rows) > 3 else "N/A")
                    
                    # Save parsed text output
                    txt_out = WORKSPACE / f"parsed_{file_path.stem}.txt"
                    with open(txt_out, "w", encoding="utf-8") as out:
                        out.write(f"Total Rows: {len(rows)}\n\n")
                        for r in rows:
                            out.write("\t".join([str(x) for x in r]) + "\n")
                    print(f"Saved parsed text to: {txt_out.name}")

    except Exception as e:
        print(f"Error parsing {file_path.name}: {e}")

if __name__ == "__main__":
    parse_xlsx(FILE_1400)
    parse_xlsx(FILE_PIPELINE)
