#!/usr/bin/env python3
"""
compile_trinity_wealth_dossier.py - Compiles Publication-Grade Trinity Wealth Scale Dossier
Generates:
  reports/TRINITY_WEALTH_SCALE_SYSTEMS.docx
  reports/TRINITY_WEALTH_SCALE_SYSTEMS.pdf
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
MODEL_PATH = DATA_DIR / "trinity_wealth_scale_model.json"

DOCX_OUT = REPORTS_DIR / "TRINITY_WEALTH_SCALE_SYSTEMS.docx"
PDF_OUT = REPORTS_DIR / "TRINITY_WEALTH_SCALE_SYSTEMS.pdf"

# Executive Sovereign Palette: Slate, Emerald, Cyan, Purple
COLOR_PRIMARY = RGBColor(16, 185, 129)    # Emerald
COLOR_SECONDARY = RGBColor(15, 23, 42)    # Slate 900
COLOR_MUTED = RGBColor(100, 116, 139)     # Slate 500
COLOR_CYAN = RGBColor(6, 182, 212)        # Cyan
COLOR_PURPLE = RGBColor(139, 92, 246)     # Purple
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
    if level == 1:
        run.font.size = Pt(18)
        run.font.color.rgb = COLOR_SECONDARY
    elif level == 2:
        run.font.size = Pt(14)
        run.font.color.rgb = COLOR_PRIMARY
    elif level == 3:
        run.font.size = Pt(12)
        run.font.color.rgb = COLOR_CYAN
    return p

def format_table_header(row, col_names, col_widths=None):
    for idx, name in enumerate(col_names):
        cell = row.cells[idx]
        set_cell_shading(cell, COLOR_HEADER_BG)
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(name)
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(255, 255, 255)
        if col_widths and idx < len(col_widths):
            cell.width = col_widths[idx]

def format_data_row(row, values, is_alt=False, col_widths=None):
    for idx, val in enumerate(values):
        cell = row.cells[idx]
        if is_alt:
            set_cell_shading(cell, COLOR_BG_SHADE)
        set_cell_margins(cell, top=90, bottom=90, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(str(val))
        run.font.size = Pt(9)
        run.font.color.rgb = COLOR_SECONDARY
        if col_widths and idx < len(col_widths):
            cell.width = col_widths[idx]

def build_dossier():
    print("[+] Loading Trinity model from:", MODEL_PATH)
    with open(MODEL_PATH, "r", encoding="utf-8") as f:
        model = json.load(f)

    doc = Document()

    # Page Margins: 0.75 in
    for s in doc.sections:
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)

    # Document Header / Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    run_t = title_p.add_run("THE TRINITY WEALTH SCALE BLUEPRINT")
    run_t.bold = True
    run_t.font.size = Pt(24)
    run_t.font.color.rgb = COLOR_SECONDARY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(12)
    run_sub = sub_p.add_run("Autonomous Multi-Tier Capital Unification: Millions ($1M-$100M) • Billions ($1B-$100B) • Trillions ($1,472T)")
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = COLOR_MUTED

    # Meta Box
    meta_table = doc.add_table(rows=1, cols=4)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_row = meta_table.rows[0]
    meta_data = [
        ("FOUNDER", "Aditya Mehra\nBBA Int'l Business '26"),
        ("HEADQUARTERS", "Bengaluru Tech Hub\nKarnataka, India"),
        ("ACTIVE PIPELINE", "$2,239,200 USD\n(96 Enterprise Accounts)"),
        ("GLOBAL POOL", "$1,472.0 Trillion USD\n(8 Planetary Pillars)")
    ]
    for idx, (label, val) in enumerate(meta_data):
        cell = meta_row.cells[idx]
        set_cell_shading(cell, "F1F5F9")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        r1 = p.add_run(f"{label}\n")
        r1.bold = True
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = COLOR_MUTED
        r2 = p.add_run(val)
        r2.bold = True
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_SECONDARY
        cell.width = Inches(1.75)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Section 1: Executive Thesis
    add_header_paragraph(doc, "1. Executive Sovereign Thesis & Trinity Architecture", 1)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.add_run(
        "Modern wealth compounding does not operate in fragmented silos; it functions as a recursive three-tiered continuum. "
        "The Trinity Scale Wealth Engine bridges micro-operational day-to-day cashflow ($1M-$100M ARR), meso-institutional promoter family offices ($1B-$100B Net Worth), "
        "and macro-planetary liquidity conduits ($1,472 Trillion total global pools). By anchoring on zero-payroll agentic architecture, "
        "the founder extracts high-margin cashflow from Tier 1, secures strategic advisory equity in Tier 2, and positions algorithmic data arteries across Tier 3."
    )

    # Section 2: Tier 1 - The Millions Engine
    add_header_paragraph(doc, "2. Tier 1: Micro-Operational Cashflow Engine ($1M - $100M ARR)", 1)
    t1 = model["matrix"]["millions_tier"]
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.add_run(
        f"Scope: {t1['scope']} | Scale Range: {t1['scale_range']}\n"
        f"Active Accounts in Funnel: {t1['active_pipeline_accounts']} | Identified Pipeline ACV: ${float(t1['pipeline_acv_usd']):,.2f} USD | "
        f"Reconciled Monthly Cashflow: INR {float(t1['active_monthly_cashflow_inr']):,.2f}/mo | Net Operating Margin: {t1['economic_margin']}"
    )

    t1_table = doc.add_table(rows=1, cols=3)
    t1_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_header(t1_table.rows[0], ["Core Competency", "System Deliverable", "Monetization Framework"], [Inches(2.2), Inches(2.8), Inches(2.0)])
    t1_competencies = [
        ("Cross-Border EXIM Optimization", "HS Code 8471.50 customs reclassification & FTP advance authorization audits", "15-20% gainshare on verified duty savings"),
        ("Autonomous Workflow Engineering", "Self-hosted n8n lead enrichment, vetting & cold outreach DAGs (32 nodes)", "Recurring monthly managed service retainer"),
        ("Founder Retainer Agreements", "Standard Master Services Agreement (MSA) with INR 351,050/mo baseline scope", "Multi-month prepaid bank wire / escrow"),
        ("Zero-Payroll Economics", "Agentic pair-programming & headless automation replacing 12 FTE personnel", "97.2% net operational EBITDA margin")
    ]
    for idx, item in enumerate(t1_competencies):
        row = t1_table.add_row()
        format_data_row(row, item, is_alt=(idx % 2 == 1), col_widths=[Inches(2.2), Inches(2.8), Inches(2.0)])

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Section 3: Tier 2 - The Billions Engine
    add_header_paragraph(doc, "3. Tier 2: Meso-Institutional Promoter Engine ($1B - $100B Net Worth)", 1)
    t2 = model["matrix"]["billions_tier"]
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.add_run(
        f"Scope: {t2['scope']} | Total Indexed Sovereign Entities: {t2['indexed_entities']}\n"
        f"Arbitrage Role: {t2['founder_arbitrage_role']}"
    )

    t2_table = doc.add_table(rows=1, cols=4)
    t2_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_header(t2_table.rows[0], ["Promoter / Office", "Hub", "Key Sectors", "Strategic Alignment Corridor"], [Inches(1.8), Inches(1.2), Inches(2.0), Inches(2.0)])
    t2_ecosystems = [
        ("PremjiInvest (Azim Premji)", "Bengaluru", "Wipro, Tech PE, Enterprise SaaS", "IT services automated procurement & compliance"),
        ("Catamaran Ventures (Murthy)", "Bengaluru", "Infosys, Cloud, Retail, CleanTech", "Cross-border logistics & supply chain modernization"),
        ("Rainmatter Capital (N. Kamath)", "Bengaluru", "Zerodha, FinTech, WealthTech", "Micro-clearing APIs & high-volume financial pipes"),
        ("Gruhas Proptech (Nikhil Kamath)", "Bengaluru", "Real Estate, PropTech, Hospitality", "Industrial logistics warehousing & land banks"),
        ("Reliance Industries (Ambani)", "Mumbai", "Jio, Retail, Petrochemicals, Green H2", "Mega-scale distribution & sovereign AI infrastructure"),
        ("Tata Sons (Chandrasekaran)", "Mumbai", "TCS, Tata Motors, Steel, Electronics", "Industrial automotive & semiconductor fab networks"),
        ("Adani Enterprises (Adani)", "Ahmedabad", "Ports, Energy, Airports, Mining", "Port logistics customs automation & bonded zones")
    ]
    for idx, item in enumerate(t2_ecosystems):
        row = t2_table.add_row()
        format_data_row(row, item, is_alt=(idx % 2 == 1), col_widths=[Inches(1.8), Inches(1.2), Inches(2.0), Inches(2.0)])

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Section 4: Tier 3 - The Trillions Engine
    add_header_paragraph(doc, "4. Tier 3: Macro-Planetary Liquidity Pillars ($1,472 Trillion USD)", 1)
    t3 = model["matrix"]["trillions_tier"]
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.add_run(
        f"Total Global Pillars Mapped: {t3['total_pillars']} | Aggregated Capital Pool: ${float(t3['total_mapped_usd']):,.1f} Trillion USD\n"
        "Global capital pools represent systemic planetary energy. The sovereign entrepreneur does not need to own these pools; "
        "one merely constructs frictionless toll gates, compliance verifiers, and automated routing pipelines along their arterial paths."
    )

    t3_table = doc.add_table(rows=1, cols=3)
    t3_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_header(t3_table.rows[0], ["Global Capital Pillar", "Mapped Liquidity Pool", "Strategic Sovereign Extraction Role"], [Inches(2.5), Inches(1.8), Inches(2.7)])
    t3_roles = [
        "Clearing house settlement fees, basis spread extraction, collateral custody",
        "REIT packaging, tokenized physical debt syndication, logistics park audits",
        "Multi-family office wealthtech advisory, AUM pipeline automation, custody routing",
        "Bond issuance structuring, sovereign debt verification, commercial paper settlement",
        "Promoter equity stake hedging, secondary block placements, automated filings",
        "Cross-border EXIM customs duty savings, Letters of Credit factoring, tariff audits",
        "Bilateral infrastructure co-investment, energy & semiconductor syndications",
        "Secondary liquidity matching, tech portfolio AI automation audits, growth advisory"
    ]
    for idx, p_item in enumerate(t3["pillars_breakdown"]):
        row = t3_table.add_row()
        format_data_row(row, [
            p_item["name"],
            p_item["scale"],
            t3_roles[idx] if idx < len(t3_roles) else "Algorithmic data routing"
        ], is_alt=(idx % 2 == 1), col_widths=[Inches(2.5), Inches(1.8), Inches(2.7)])

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Section 5: Strategic Synthesis & Roadmap
    add_header_paragraph(doc, "5. Sovereign Compounding Roadmap (2026 - 2030)", 1)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.add_run(
        "Phase 1 (Months 1-6): Scale Tier 1 ARR to $1,000,000 USD via 15 enterprise EXIM trade optimization retainers.\n"
        "Phase 2 (Months 6-18): Secure 3 Tier 2 family office strategic technology partnerships, taking 5-10% performance carry in lieu of advisory fees.\n"
        "Phase 3 (Months 18-36): Deploy institutional micro-clearing protocol across Tier 3 trade arteries, settling $100M+ in cross-border paper autonomously.\n"
        "Phase 4 (Perpetual): Infinite compounding with 97%+ net EBITDA channeled into sovereign infrastructure and AI compute assets."
    )

    # Save DOCX
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    doc.save(DOCX_OUT)
    print(f"[OK] Generated Word Dossier: {DOCX_OUT}")

    # Convert to PDF via Word COM
    try:
        import win32com.client
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        doc_obj = word.Documents.Open(str(DOCX_OUT))
        doc_obj.SaveAs(str(PDF_OUT), FileFormat=17) # 17 = wdFormatPDF
        doc_obj.Close()
        word.Quit()
        print(f"[OK] Converted to PDF Dossier: {PDF_OUT}")
    except Exception as e:
        print(f"[!] Word COM conversion warning: {e}")

if __name__ == "__main__":
    build_dossier()
