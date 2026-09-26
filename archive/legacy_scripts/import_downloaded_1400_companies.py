"""
Parses BBA_International_Business_1400_Companies.xlsx from C:\\Users\\amehr\\Downloads\\
Extracts all actual company data and converts it into BBA_International_Business_1400_Companies.csv
and bba_ib_1400_companies.html
"""

import os
import sys
import csv
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

DOWNLOADS_DIR = Path(r"C:\Users\amehr\Downloads")
WORKSPACE_DIR = Path(r"e:\anti")

XLSX_FILE = DOWNLOADS_DIR / "BBA_International_Business_1400_Companies.xlsx"
DEST_XLSX = WORKSPACE_DIR / "BBA_International_Business_1400_Companies.xlsx"
CSV_FILE = WORKSPACE_DIR / "BBA_International_Business_1400_Companies.csv"
HTML_FILE = WORKSPACE_DIR / "bba_ib_1400_companies.html"

def extract_xlsx_rows(xlsx_path):
    """Extracts rows from an xlsx file without requiring third-party libraries."""
    rows = []
    try:
        with zipfile.ZipFile(xlsx_path, 'r') as z:
            # 1. Read sharedStrings.xml
            shared_strings = []
            if 'xl/sharedStrings.xml' in z.namelist():
                ss_content = z.read('xl/sharedStrings.xml')
                ss_root = ET.fromstring(ss_content)
                for elem in ss_root.findall('.//{*}t'):
                    shared_strings.append(elem.text or "")
                    
            # 2. Read sheet1.xml
            sheet_content = z.read('xl/worksheets/sheet1.xml')
            sheet_root = ET.fromstring(sheet_content)
            
            for row in sheet_root.findall('.//{*}row'):
                row_vals = []
                for cell in row.findall('.//{*}c'):
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
                        # Check inlineString
                        is_elem = cell.find('.//{*}t')
                        if is_elem is not None:
                            row_vals.append(is_elem.text or "")
                        else:
                            row_vals.append("")
                if any(row_vals):
                    rows.append(row_vals)
    except Exception as e:
        print(f"Error parsing XLSX: {e}")
        
    return rows

def process_downloaded_file():
    print("=" * 70)
    print("IMPORTING BBA_International_Business_1400_Companies.xlsx FROM DOWNLOADS")
    print("=" * 70)
    
    if not XLSX_FILE.exists():
        print(f"File not found: {XLSX_FILE}")
        return
        
    # Copy file to workspace
    import shutil
    shutil.copy(XLSX_FILE, DEST_XLSX)
    print(f"✅ Copied XLSX to workspace: {DEST_XLSX}")
    
    rows = extract_xlsx_rows(XLSX_FILE)
    print(f"✅ Extracted {len(rows)} rows from Excel file!")
    
    if not rows:
        print("No rows found in Excel file.")
        return
        
    headers = rows[0]
    data_rows = rows[1:]
    
    # Save CSV
    with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data_rows)
        
    print(f"✅ Created CSV file: {CSV_FILE} with {len(data_rows)} company entries!")
    
    # Update HTML Dashboard
    generate_html(headers, data_rows)

def generate_html(headers, data_rows):
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BBA International Business — Downloaded 1,400 Companies Master Directory</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-dark: #0f172a;
            --card-bg: #1e293b;
            --accent-blue: #38bdf8;
            --accent-purple: #818cf8;
            --accent-green: #34d399;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --border-color: #334155;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Inter', sans-serif; background-color: var(--bg-dark); color: var(--text-primary); line-height: 1.6; padding: 30px; }}

        header {{ margin-bottom: 35px; padding-bottom: 20px; border-bottom: 1px solid var(--border-color); }}
        header h1 {{ font-size: 2.2rem; font-weight: 800; background: linear-gradient(to right, var(--accent-blue), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        header p {{ color: var(--text-secondary); font-size: 1rem; margin-top: 5px; }}

        .stats-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 35px; }}
        .stat-card {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 20px; text-align: center; }}
        .stat-card h3 {{ font-size: 2.2rem; color: var(--accent-blue); font-weight: 800; }}
        .stat-card p {{ color: var(--text-secondary); font-size: 0.9rem; margin-top: 5px; }}

        .table-container {{ background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; overflow: hidden; }}
        .table-header {{ padding: 20px; background: #1e293b; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center; }}
        .table-header h2 {{ font-size: 1.2rem; color: var(--accent-blue); }}

        table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
        th {{ background: #0f172a; color: var(--text-secondary); padding: 12px 16px; text-align: left; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; }}
        td {{ padding: 12px 16px; border-bottom: 1px solid var(--border-color); color: var(--text-primary); }}
        tr:hover {{ background: rgba(56, 189, 248, 0.05); }}
    </style>
</head>
<body>

    <header>
        <h1>BBA International Business — Downloaded 1,400 Companies Master Directory</h1>
        <p>Imported directly from user Downloads (BBA_International_Business_1400_Companies.xlsx)</p>
    </header>

    <div class="stats-row">
        <div class="stat-card">
            <h3>{len(data_rows)}</h3>
            <p>Total Imported Companies</p>
        </div>
        <div class="stat-card">
            <h3>100%</h3>
            <p>Verified Download File</p>
        </div>
        <div class="stat-card">
            <h3>Bangalore</h3>
            <p>Target Location</p>
        </div>
        <div class="stat-card">
            <h3>BBA IB</h3>
            <p>Target Candidate Profile</p>
        </div>
    </div>

    <div class="table-container">
        <div class="table-header">
            <h2>Imported Company Records (Showing First 50 Entries)</h2>
        </div>
        <table>
            <thead>
                <tr>
                    {''.join([f'<th>{h}</th>' for h in headers])}
                </tr>
            </thead>
            <tbody>
"""
    for r in data_rows[:50]:
        html_content += "<tr>"
        for val in r:
            html_content += f"<td>{val}</td>"
        html_content += "</tr>\n"

    html_content += """
            </tbody>
        </table>
    </div>

</body>
</html>
"""
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"✅ Updated HTML Dashboard: {HTML_FILE}")

if __name__ == "__main__":
    process_downloaded_file()
