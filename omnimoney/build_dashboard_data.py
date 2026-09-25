"""
Generates static JS data bundle for OMNIMONEY_RADAR_BENGALURU.html
"""

import json
import os
from omnimoney.omnimoney_engine import OmniMoneyEngine
from omnimoney.b2b_sales_engine import B2BSalesEngine

def build_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    engine = OmniMoneyEngine()
    sales = B2BSalesEngine()

    dashboard_data = engine.export_dashboard_data()
    dashboard_data["crm_pipeline"] = {
        "summary": sales.get_pipeline_summary(),
        "prospects": [p.__dict__ for p in sales.get_prospects()]
    }

    out_file = os.path.join(base_dir, "omnimoney_data.js")
    js_content = f"window.OMNIMONEY_DATA = {json.dumps(dashboard_data, indent=2)};\n"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"Generated {out_file} ({len(js_content)} bytes)")

main = build_data

if __name__ == "__main__":
    build_data()
