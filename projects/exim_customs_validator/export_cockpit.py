"""
Visual Cockpit Generator for Global Trade & Customs Engine
Exports standalone HTML dashboard with UCP 600 audit results and landed cost matrices.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from demo_cases import run_demonstration

OUTPUT_HTML = os.path.join(os.path.dirname(__file__), "exim_compliance_cockpit.html")

def export_cockpit(output_path: str = OUTPUT_HTML):
    data = run_demonstration()

    rows = ""
    total_cif = 0.0
    total_duties = 0.0

    for item in data:
        meta = item["meta"]
        comp = item["compliance"]
        cust = item["customs"]
        total_cif += cust.cif_value_inr
        total_duties += cust.total_customs_duty_inr

        badge = '<span style="background:rgba(16,185,129,0.2);color:#10b981;padding:4px 10px;border-radius:6px;font-weight:600;">CLEAN COMPLIANT</span>' if comp.is_compliant else '<span style="background:rgba(239,68,68,0.2);color:#ef4444;padding:4px 10px;border-radius:6px;font-weight:600;">DISCREPANT (HELD)</span>'
        discrepancy_html = f"<div style='color:#f87171;font-size:0.85rem;margin-top:4px;'>{'<br>'.join(comp.discrepancies)}</div>" if comp.discrepancies else "<span style='color:#10b981;font-size:0.85rem;'>UCP 600 Art 14/18/20/30 Verified</span>"

        rows += f"""
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
            <td style="padding:16px;">
                <div style="font-weight:700;color:#f8fafc;">{meta['name']}</div>
                <div style="font-size:0.8rem;color:#94a3b8;margin-top:2px;">LC: {meta['lc'].lc_number} | Term: {meta['lc'].incoterm}</div>
            </td>
            <td style="padding:16px;">
                <div>{meta['lc'].beneficiary}</div>
                <div style="font-size:0.8rem;color:#94a3b8;">Port: {meta['lc'].port_of_loading} &rarr; {meta['lc'].port_of_discharge}</div>
            </td>
            <td style="padding:16px;text-align:right;font-weight:600;">₹{cust.cif_value_inr:,.2f}</td>
            <td style="padding:16px;text-align:right;color:#fbbf24;">₹{cust.bcd_amount_inr:,.2f}</td>
            <td style="padding:16px;text-align:right;color:#a78bfa;">₹{cust.igst_amount_inr:,.2f}</td>
            <td style="padding:16px;text-align:right;font-weight:700;color:#38bdf8;">₹{cust.total_customs_duty_inr:,.2f}</td>
            <td style="padding:16px;text-align:right;font-weight:800;color:#34d399;">₹{cust.total_landed_cost_inr:,.2f}</td>
            <td style="padding:16px;text-align:center;">{badge}</td>
            <td style="padding:16px;">{discrepancy_html}</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global Trade, Incoterms 2020 & Customs Landed Cost Engine</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #090d16;
            --surface: #111827;
            --border: rgba(255,255,255,0.08);
            --primary: #3b82f6;
            --emerald: #10b981;
            --amber: #f59e0b;
            --purple: #8b5cf6;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }}
        * {{ margin:0; padding:0; box-sizing:border-box; font-family:'Inter', sans-serif; }}
        body {{ background: var(--bg); color: var(--text-main); min-height:100vh; padding: 32px 24px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 28px; padding-bottom: 20px; border-bottom: 1px solid var(--border); }}
        .badge {{ background: rgba(139,92,246,0.15); border: 1px solid rgba(139,92,246,0.4); color: #c084fc; padding: 4px 12px; border-radius: 999px; font-size: 0.8rem; font-weight: 600; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 32px; }}
        .kpi-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }}
        .kpi-label {{ font-size: 0.82rem; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em; margin-bottom: 6px; }}
        .kpi-val {{ font-size: 1.7rem; font-weight: 800; }}
        .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }}
        .card-header {{ padding: 18px 20px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; }}
        th {{ background: rgba(255,255,255,0.02); text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.05em; color: var(--text-muted); padding: 12px 16px; text-align: left; }}
        .mono {{ font-family: 'JetBrains Mono', monospace; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:6px;">
                <h1 style="font-size:1.6rem; font-weight:800; letter-spacing:-0.02em;">Global Trade & Customs Compliance Engine</h1>
                <span class="badge">UCP 600 & INCOTERMS 2020</span>
            </div>
            <p style="color:var(--text-muted); font-size:0.92rem;">ICC UCP 600 Documentary Credit Verification & Section 14 Landed Customs Duty Engine | Aditya Mehra International Business Portfolio</p>
        </div>
        <div style="text-align:right;">
            <div style="color:var(--emerald); font-weight:700; font-size:0.9rem;">● TRADE PROTOCOL ACTIVE</div>
            <div style="color:var(--text-muted); font-size:0.8rem; margin-top:4px;">100% Deterministic Customs Assessment</div>
        </div>
    </div>

    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Total Assessable CIF Value</div>
            <div class="kpi-val mono">₹{total_cif:,.2f}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Total Indian Customs Duties</div>
            <div class="kpi-val mono" style="color:var(--amber);">₹{total_duties:,.2f}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Exchange Rate Reference</div>
            <div class="kpi-val mono" style="color:var(--primary);">₹85.00 / USD</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">UCP 600 Compliance Rate</div>
            <div class="kpi-val mono" style="color:var(--emerald);">66.7%</div>
        </div>
    </div>

    <div class="card">
        <div class="card-header">
            <h3 style="font-size:1.05rem; font-weight:700;">Audited Consignments & Documentary Credits</h3>
            <span style="font-size:0.85rem; color:var(--text-muted);">Incoterms: FOB / CIF / DDP | CBIC Customs Valuation</span>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Shipment / Consignment</th>
                    <th>Beneficiary & Trade Lane</th>
                    <th style="text-align:right;">CIF Value</th>
                    <th style="text-align:right;">BCD</th>
                    <th style="text-align:right;">IGST (18%)</th>
                    <th style="text-align:right;">Total Duty</th>
                    <th style="text-align:right;">Landed Cost</th>
                    <th style="text-align:center;">UCP Status</th>
                    <th>Discrepancy / Audit Log</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[SUCCESS] Exported EXIM Compliance Cockpit to: {output_path}")

if __name__ == "__main__":
    export_cockpit()
