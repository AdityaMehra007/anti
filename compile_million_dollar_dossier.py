#!/usr/bin/env python3
"""
compile_million_dollar_dossier.py - Compiles Publication-Grade $1,000,000 ARR Sovereign Enterprise Blueprint
Generates:
  reports/MILLION_DOLLAR_ENTERPRISE_BLUEPRINT.docx
  reports/MILLION_DOLLAR_ENTERPRISE_BLUEPRINT.pdf
"""

import sys
import os
import json
import sqlite3
from datetime import datetime, date
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

ROOT_DIR = Path(r"e:\anti")
DATA_DIR = ROOT_DIR / "data"
REPORTS_DIR = ROOT_DIR / "reports"
DB_PATH = DATA_DIR / "omega_unified_master.db"
MODEL_PATH = DATA_DIR / "million_dollar_company_model.json"

DOCX_OUT = REPORTS_DIR / "MILLION_DOLLAR_ENTERPRISE_BLUEPRINT.docx"
PDF_OUT = REPORTS_DIR / "MILLION_DOLLAR_ENTERPRISE_BLUEPRINT.pdf"

# Emerald Gold Executive Sovereign Palette
COLOR_PRIMARY = RGBColor(16, 185, 129)   # Emerald 500
COLOR_SECONDARY = RGBColor(15, 23, 42)   # Slate 900
COLOR_MUTED = RGBColor(100, 116, 139)    # Slate 500
COLOR_ACCENT = RGBColor(14, 165, 233)    # Sky 500
COLOR_BORDER = "CBD5E1"
COLOR_BG_SHADE = "F8FAFC"
COLOR_HEADER_BG = "0F172A"

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def add_header_paragraph(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Calibri"
    if level == 1:
        run.font.size = Pt(16)
        run.font.color.rgb = COLOR_SECONDARY
    elif level == 2:
        run.font.size = Pt(13)
        run.font.color.rgb = COLOR_PRIMARY
    return p

def format_cell_text(cell, text, bold=False, color_rgb=None, font_size_pt=9.5, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(str(text))
    run.bold = bold
    run.font.name = "Calibri"
    run.font.size = Pt(font_size_pt)
    if color_rgb:
        run.font.color.rgb = color_rgb

def build_docx():
    print("[1/2] Building Million-Dollar Sovereign Enterprise Word Document...")
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    with open(MODEL_PATH, "r", encoding="utf-8") as f:
        model = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT company_name, tier, target_service, annual_contract_value_usd, win_probability, expected_value_usd 
        FROM million_dollar_pipeline 
        ORDER BY annual_contract_value_usd DESC 
        LIMIT 10
    """)
    top_deals = c.fetchall()
    conn.close()

    curr = model["currency_targets"]
    econ = model["unit_economics"]
    val = model["enterprise_valuation"]

    # Header
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    run_t = title_p.add_run("THE $1,000,000 ARR SOVEREIGN ENTERPRISE")
    run_t.bold = True
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(22)
    run_t.font.color.rgb = COLOR_SECONDARY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(14)
    run_sub = sub_p.add_run("Master Operational Roadmap, Unit Economics & Autonomous Swarm Capitalization\nFounder: Aditya Mehra | Bengaluru, Karnataka, India")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = COLOR_PRIMARY

    # Executive Summary
    add_header_paragraph(doc, "1. Executive Summary & $1M ARR Valuation Model", 1)
    p_lead = doc.add_paragraph()
    p_lead.paragraph_format.line_spacing = 1.15
    run_lead = p_lead.add_run(
        "This master specification establishes the operational blueprint for scaling Aditya Mehra Global Autonomous Solutions (AMG Solutions) "
        "to $1,000,000 Annual Recurring Revenue (ARR) ($84,000 / ~INR 71.4 Lakhs monthly run-rate; ~INR 8.57 Crores ARR). "
        "Operating with a 5-agent autonomous swarm and leveraging deep domain authority in International Trade & Incoterms 2020 cross-border logistics, "
        "the enterprise operates at an extraordinary 97.5% EBITDA net margin with zero payroll overhead, commanding an institutional valuation of $7.56 Million (~INR 64.2 Crores)."
    )
    run_lead.font.name = "Calibri"
    run_lead.font.size = Pt(10)

    # Master Financial Metrics
    add_header_paragraph(doc, "2. High-Yield Capital Architecture & Valuation", 1)
    tbl_kpi = doc.add_table(rows=6, cols=2)
    tbl_kpi.alignment = WD_TABLE_ALIGNMENT.CENTER
    kpis = [
        ("Annual Recurring Revenue (ARR Target)", f"${curr['arr_usd']:,.0f} USD (INR {curr['arr_inr'] / 1e7:,.2f} Crore / Year)"),
        ("Monthly Recurring Revenue (MRR)", f"${curr['mrr_usd']:,.0f} USD (INR {curr['mrr_inr']:,.0f} / Month)"),
        ("Net Annual EBITDA Profit", f"${econ['annual_net_profit_usd']:,.0f} USD (INR {econ['annual_net_profit_inr'] / 1e7:,.2f} Crore)"),
        ("EBITDA Operating Margin", f"{econ['ebitda_margin_pct']}% (Zero Payroll Overhead)"),
        ("Target Enterprise Valuation (7.5x Multiple)", f"${val['valuation_usd']:,.0f} USD (INR {val['valuation_inr'] / 1e7:,.2f} Crore Valuation)"),
        ("Active Corporate Account Capacity", "43 Paying Enterprise Accounts across 3 Tiers")
    ]
    for idx, (lbl, v) in enumerate(kpis):
        r = tbl_kpi.rows[idx]
        c_lbl, c_val = r.cells[0], r.cells[1]
        set_cell_margins(c_lbl, 80, 80, 120, 120)
        set_cell_margins(c_val, 80, 80, 120, 120)
        set_cell_shading(c_lbl, COLOR_BG_SHADE)
        format_cell_text(c_lbl, lbl, bold=True, color_rgb=COLOR_SECONDARY)
        format_cell_text(c_val, v, bold=True, color_rgb=COLOR_PRIMARY)

    # Portfolio Distribution
    add_header_paragraph(doc, "3. Three-Tier Product & Service Portfolio", 1)
    p_tiers = doc.add_paragraph()
    p_tiers.paragraph_format.line_spacing = 1.15
    p_tiers.add_run(
        "• Tier 1: Enterprise Trade Landed-Cost & Customs Compliance Retainers (10 Clients @ $3,500/mo = $35,000/mo / $420k ARR)\n"
        "  Targeted at mid-to-large Indian and global freight forwarders, electronics importers, and manufacturing conglomerates needing Incoterms 2020 tariff audits and bonded warehouse concessions.\n\n"
        "• Tier 2: Enterprise Agentic AI & Self-Healing n8n Pipeline Suites (20 Clients @ $1,800/mo = $36,000/mo / $432k ARR)\n"
        "  Targeted at tech scaleups, SaaS platforms, and fulfillment companies automating invoice reconciliation, webhook triggers, and autonomous SLA governance.\n\n"
        "• Tier 3: High-Yield Recruiter & Candidate Intelligence Licenses (13 Clients @ $1,000/mo = $13,000/mo / $156k ARR)\n"
        "  Targeted at executive talent acquisition teams seeking curated access to 17,615+ vetted early-career engineering profiles and direct outreach DAGs."
    )

    # Top Deal Pipeline Table
    add_header_paragraph(doc, "4. Enterprise Deal Pipeline Sample (From 17,615 Master DB)", 1)
    tbl_deals = doc.add_table(rows=len(top_deals) + 1, cols=4)
    tbl_deals.alignment = WD_TABLE_ALIGNMENT.CENTER
    d_headers = ["Enterprise Account", "Contract Tier", "Annual Contract Value", "Win-Weighted ARR"]
    for j, h in enumerate(d_headers):
        cell = tbl_deals.rows[0].cells[j]
        set_cell_margins(cell, 100, 100, 120, 120)
        set_cell_shading(cell, COLOR_HEADER_BG)
        format_cell_text(cell, h, bold=True, color_rgb=RGBColor(255, 255, 255))
        
    for i, d in enumerate(top_deals):
        row = tbl_deals.rows[i + 1]
        comp, tier, svc, acv, prob, ev = d
        for j, val in enumerate([comp, tier.replace('TIER_', ''), f"${acv:,.0f} USD", f"${ev:,.0f} USD"]):
            cell = row.cells[j]
            set_cell_margins(cell, 80, 80, 120, 120)
            if i % 2 == 1:
                set_cell_shading(cell, COLOR_BG_SHADE)
            format_cell_text(cell, val, bold=(j == 0 or j == 3), color_rgb=COLOR_SECONDARY)

    # Execution Directives
    add_header_paragraph(doc, "5. Sovereign Execution Directives for Founder Aditya Mehra", 1)
    p_ex = doc.add_paragraph()
    p_ex.paragraph_format.line_spacing = 1.15
    p_ex.add_run(
        "1. Autonomous Outbound Compounding: Maintain enterprise_daemon.py in continuous operation, refreshing 50 high-ticket B2B leads daily.\n"
        "2. Deterministic Fulfillment: Deploy standardized client blueprints within 48 hours of onboarding using modular n8n workflows and automated Excel landed cost models.\n"
        "3. Capital Reinvestment & Moat Construction: Compound net cashflow into proprietary datasets, sovereign AI infrastructure, and institutional brand authority."
    )

    doc.save(DOCX_OUT)
    print(f"[OK] Saved Million-Dollar Blueprint Word Document: {DOCX_OUT}")

def convert_to_pdf():
    print("[2/2] Exporting Million-Dollar Blueprint to PDF via Word COM...")
    try:
        import win32com.client
        import pythoncom
        pythoncom.CoInitialize()
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = False
        doc = word.Documents.Open(str(DOCX_OUT.resolve()))
        doc.SaveAs(str(PDF_OUT.resolve()), FileFormat=17)
        doc.Close(False)
        word.Quit()
        print(f"[OK] Successfully exported PDF: {PDF_OUT}")
    except Exception as e:
        print(f"[!] Warning: Word COM export failed: {e}")

if __name__ == "__main__":
    build_docx()
    convert_to_pdf()
