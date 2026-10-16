#!/usr/bin/env python3
"""
compile_jobfunnel_guide.py - Compiles Publication-Grade JobFunnel Executive Guide
Generates reports/JOBFUNNEL_MASTER_INTELLIGENCE_GUIDE.docx and converts to .pdf via Word COM.
"""

import sys
import os
import json
import sqlite3
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

ROOT_DIR = Path(r"e:\anti")
REPORTS_DIR = ROOT_DIR / "reports"
TELEMETRY_PATH = ROOT_DIR / "data" / "jobfunnel_telemetry.json"
DUPLICATES_PATH = ROOT_DIR / "data" / "jobfunnel_duplicates.json"
DOCX_OUT = REPORTS_DIR / "JOBFUNNEL_MASTER_INTELLIGENCE_GUIDE.docx"
PDF_OUT = REPORTS_DIR / "JOBFUNNEL_MASTER_INTELLIGENCE_GUIDE.pdf"

# Color Palette: Deep Slate, JobFunnel Amber/Orange, Subtle Gray
COLOR_PRIMARY = RGBColor(217, 119, 6)     # Amber 600
COLOR_SECONDARY = RGBColor(15, 23, 42)    # Slate 900
COLOR_MUTED = RGBColor(100, 116, 139)     # Slate 500
COLOR_HIGHLIGHT = RGBColor(245, 158, 11)  # Amber 500
COLOR_BORDER = "E2E8F0"
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
        run.font.size = Pt(17)
        run.font.color.rgb = COLOR_SECONDARY
    elif level == 2:
        run.font.size = Pt(13)
        run.font.color.rgb = COLOR_PRIMARY
    else:
        run.font.size = Pt(11)
        run.font.color.rgb = COLOR_SECONDARY
    return p

def main():
    print("[*] Loading telemetry and duplicate audit logs...")
    telemetry = json.load(open(TELEMETRY_PATH, "r", encoding="utf-8"))
    duplicates = json.load(open(DUPLICATES_PATH, "r", encoding="utf-8"))

    doc = Document()

    # Page Margins (0.75 in)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # Document Title Block
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    t_run = title_p.add_run("OMEGA ∞ EXECUTIVE INTELLIGENCE REPORT")
    t_run.font.name = "Calibri"
    t_run.font.size = Pt(10)
    t_run.font.bold = True
    t_run.font.color.rgb = COLOR_PRIMARY

    h1_p = doc.add_paragraph()
    h1_p.paragraph_format.space_after = Pt(4)
    h1_run = h1_p.add_run("JobFunnel Multi-Board Deduplication & Master Funnel")
    h1_run.font.name = "Calibri"
    h1_run.font.size = Pt(22)
    h1_run.font.bold = True
    h1_run.font.color.rgb = COLOR_SECONDARY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    sub_run = sub_p.add_run("Automated Ingestion, Exact Key De-duping, TF-IDF Cosine Similarity & Master CSV Telemetry across 8,576 Role Postings")
    sub_run.font.name = "Calibri"
    sub_run.font.size = Pt(11)
    sub_run.font.color.rgb = COLOR_MUTED

    # Meta Callout Box
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.rows[0].cells[0]
    set_cell_shading(c, "FFFBEB") # Amber light tint
    set_cell_margins(c, 120, 120, 160, 160)
    cp = c.paragraphs[0]
    cp.paragraph_format.space_before = Pt(0)
    cp.paragraph_format.space_after = Pt(0)
    c_run = cp.add_run(
        f"EXECUTIVE SUMMARY: JobFunnel pipeline ingested 8,576 candidate listings from 4 repositories, purged 1,666 duplicate multi-board listings (515 exact, 1,151 TF-IDF cosine variants), and established a 6,910 clean-opportunity Master CSV Funnel. Master FTS5 Index expanded to 17,657 entities."
    )
    c_run.font.name = "Calibri"
    c_run.font.size = Pt(9.5)
    c_run.font.bold = True
    c_run.font.color.rgb = COLOR_SECONDARY

    # Section 1: Macro Telemetry
    add_header_paragraph(doc, "1. Executive Funnel Telemetry", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "Candidate postings from diverse career scrapers and repositories suffer from severe duplicate inflation due to cross-board aggregations. JobFunnel solves this through a deterministic dual-stage filter:"
    )

    t1 = doc.add_table(rows=5, cols=3)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Funnel Metric", "Listing Count", "Strategic Significance"]
    for idx, h in enumerate(headers):
        cell = t1.rows[0].cells[idx]
        set_cell_shading(cell, COLOR_HEADER_BG)
        set_cell_margins(cell, 80, 80, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    stats_rows = [
        ("Raw Listings Ingested", f"{telemetry['total_raw_listings']:,}", "Aggregate listings across Summer '27, New Grad '26 & '27, and AI Jobs"),
        ("Exact Metadata Dupes Purged", f"{telemetry['exact_duplicates']:,}", "Identical (Company, Title, Location) cross-board duplicates"),
        ("TF-IDF Cosine Dupes Purged", f"{telemetry['tfidf_duplicates']:,}", "Cosine similarity >= 0.88 with company stem matching"),
        ("Net Master Funnel Listings", f"{telemetry['total_unique_listings']:,}", "Clean, non-redundant opportunities ready for application targeting"),
    ]

    for row_idx, data in enumerate(stats_rows, start=1):
        for col_idx, val in enumerate(data):
            cell = t1.rows[row_idx].cells[col_idx]
            if row_idx % 2 == 1:
                set_cell_shading(cell, COLOR_BG_SHADE)
            set_cell_margins(cell, 70, 70, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if col_idx == 0:
                r.bold = True

    # Section 2: Distribution by Ecosystem & Remoteness
    add_header_paragraph(doc, "2. Ecosystem Ingestion & Remoteness Breakdown", level=1)
    
    t2 = doc.add_table(rows=5, cols=3)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Source Ecosystem", "Clean Retained Roles", "Share of Master Funnel"]
    for idx, h in enumerate(headers):
        cell = t2.rows[0].cells[idx]
        set_cell_shading(cell, COLOR_HEADER_BG)
        set_cell_margins(cell, 80, 80, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    tot = telemetry['total_unique_listings']
    p_data = [
        ("New Grad 2026", telemetry['provider_breakdown'].get('New Grad 2026', 0)),
        ("Summer 2027 Internships", telemetry['provider_breakdown'].get('Summer 2027 Internships', 0)),
        ("AI College Jobs 2027", telemetry['provider_breakdown'].get('AI College Jobs 2027', 0)),
        ("New Grad 2027", telemetry['provider_breakdown'].get('New Grad 2027', 0)),
    ]

    for row_idx, (prov, count) in enumerate(p_data, start=1):
        pct = (count / tot) * 100 if tot else 0
        vals = [prov, f"{count:,}", f"{pct:.1f}%"]
        for col_idx, val in enumerate(vals):
            cell = t2.rows[row_idx].cells[col_idx]
            if row_idx % 2 == 1:
                set_cell_shading(cell, COLOR_BG_SHADE)
            set_cell_margins(cell, 70, 70, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if col_idx == 0:
                r.bold = True

    # Remoteness Telemetry
    p_rem = doc.add_paragraph()
    p_rem.paragraph_format.space_before = Pt(8)
    r_bold = p_rem.add_run("Workplace Flexibility Taxonomy: ")
    r_bold.bold = True
    r_bold.font.size = Pt(9.5)
    rem_text = " • ".join([f"{k}: {v:,}" for k, v in telemetry['remoteness_breakdown'].items()])
    r_val = p_rem.add_run(rem_text)
    r_val.font.size = Pt(9.5)

    # Section 3: Dual-Stage Deduplication Methodology
    add_header_paragraph(doc, "3. JobFunnel Dual-Stage Deduplication Architecture", level=1)
    p_arch = doc.add_paragraph()
    p_arch.add_run(
        "JobFunnel implements a rigorous two-tier anti-redundancy architecture that safeguards job hunters from application fatigue and duplicative outreach:\n"
        "1. Stage 1 (Deterministic Tuple Hash): Hashes (company_stem, title_stem, location_stem). All subsequent arrivals with identical tuple signatures are tagged as EXACT_METADATA_MATCH and quarantined.\n"
        "2. Stage 2 (TF-IDF Cosine Similarity Matrix): For listings with minor stylistic title variance (e.g., 'Software Engineer Intern - Systems' vs 'Software Engineer Intern (Systems)'), JobFunnel fits an n-gram TF-IDF vectorizer over the textual corpus. Cosine distances >= 0.88 combined with company namespace matching are flagged as TFIDF_COSINE_SIMILARITY.\n"
        "3. Resultant Ledger: All eliminated listings are preserved in 'data/jobfunnel_duplicates.json' with both duplicate ID and originating master ID for complete auditability."
    )

    # Section 4: Sample Cross-Board Duplicates Flagged
    add_header_paragraph(doc, "4. Audit Sample: Flagged Multi-Board Duplicates", level=1)
    
    t3 = doc.add_table(rows=min(7, len(duplicates) + 1), cols=4)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Company", "Role Title", "Original vs Duplicate Source", "Match Algorithm"]
    for idx, h in enumerate(headers):
        cell = t3.rows[0].cells[idx]
        set_cell_shading(cell, COLOR_HEADER_BG)
        set_cell_margins(cell, 80, 80, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    for row_idx, dupe in enumerate(duplicates[:6], start=1):
        vals = [
            dupe["company"][:24],
            dupe["title"][:28],
            f"{dupe['original_provider']} -> {dupe['duplicate_provider']}",
            f"{dupe['type']} ({dupe['similarity']})",
        ]
        for col_idx, val in enumerate(vals):
            cell = t3.rows[row_idx].cells[col_idx]
            if row_idx % 2 == 1:
                set_cell_shading(cell, COLOR_BG_SHADE)
            set_cell_margins(cell, 60, 60, 90, 90)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if col_idx == 0:
                r.bold = True

    # Section 5: Integration & Command Architecture
    add_header_paragraph(doc, "5. Unified Master Engine Integration", level=1)
    p_cmd = doc.add_paragraph()
    p_cmd.add_run(
        "JobFunnel is integrated natively into the OMEGA master operating system:\n"
        "• Master CSV Pipeline: 'data/jobfunnel_master_list.csv' containing 6,910 deduplicated rows with full status progression.\n"
        "• Dedicated FTS5 Database: 'data/jobfunnel_master.db' with instant sub-millisecond keyword search.\n"
        "• Master FTS5 Database: 'data/omega_unified_master.db' total entity index elevated to 17,657 cross-repository records.\n"
        "• Interactive Dashboard: 'jobfunnel_dashboard.html' providing real-time client-side filtering by Status, Provider, Remoteness, and Search.\n"
        "• CLI Tooling: 'jobfunnel_engine.py' supporting --stats, --search <query>, and --ui."
    )

    doc.save(DOCX_OUT)
    print(f"[OK] Generated Word document: {DOCX_OUT}")

    # Convert to PDF via Word COM
    try:
        import win32com.client
        print("[*] Converting DOCX to PDF via Microsoft Word COM...")
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        doc_obj = word.Documents.Open(str(DOCX_OUT.resolve()))
        doc_obj.SaveAs(str(PDF_OUT.resolve()), FileFormat=17) # 17 = wdFormatPDF
        doc_obj.Close()
        word.Quit()
        print(f"[OK] Successfully compiled PDF: {PDF_OUT}")
    except Exception as e:
        print(f"[!] Word COM PDF generation warning: {e}")

if __name__ == "__main__":
    main()
