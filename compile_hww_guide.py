import os
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

companies = json.load(open(r"e:\anti\data\hiring_without_whiteboards.json", encoding="utf-8"))

doc = docx.Document()

# Page setup: Standard Margins
for section in doc.sections:
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

# Styling palette
COLOR_PRIMARY = RGBColor(15, 23, 42)     # Slate 900
COLOR_TEAL = RGBColor(13, 148, 136)      # Teal 600
COLOR_MUTED = RGBColor(100, 116, 139)    # Slate 500

# Title
title_p = doc.add_paragraph()
title_run = title_p.add_run("HIRING WITHOUT WHITEBOARDS")
title_run.font.name = "Arial"
title_run.font.size = Pt(22)
title_run.font.bold = True
title_run.font.color.rgb = COLOR_TEAL

subtitle_p = doc.add_paragraph()
sub_run = subtitle_p.add_run("Executive Engineering Directory & Real-World Assessment Playbook")
sub_run.font.name = "Arial"
sub_run.font.size = Pt(12)
sub_run.font.bold = True
sub_run.font.color.rgb = COLOR_MUTED

# Meta Callout Box
meta_p = doc.add_paragraph()
meta_run = meta_p.add_run(
    f"Catalog Scope: {len(companies)} Global Companies • 290 Remote-Friendly • 46 India Engineering Centers\n"
    "Evaluation Criteria: Real-World Take-Home Tasks • Pair Programming • Architecture & System Tradeoffs"
)
meta_run.font.name = "Calibri"
meta_run.font.size = Pt(9.5)
meta_run.font.color.rgb = RGBColor(51, 65, 85)

doc.add_paragraph() # spacer

# Section 1: Strategic Philosophy
h1 = doc.add_paragraph()
h1_run = h1.add_run("1. The Shift to Real-World Evaluation")
h1_run.font.name = "Arial"
h1_run.font.size = Pt(14)
h1_run.font.bold = True
h1_run.font.color.rgb = COLOR_PRIMARY

p1 = doc.add_paragraph()
p1.add_run(
    "Traditional whiteboard interviews rely on synthetic CS trivia, synthetic algorithm puzzles (e.g. reversing a binary tree on a blackboard), "
    "and high-anxiety brainteasers that fail to predict on-the-job engineering performance. The 767 companies in this directory replace algorithmic "
    "trivia with realistic evaluation methods:\n"
    "• Take-Home Projects: A 2 to 4 hour timeboxed real-world task that mirrors actual production codebases.\n"
    "• Pair Programming: Working alongside senior engineers on an existing bug, refactor, or feature request.\n"
    "• System Design & Architecture: Whiteboarding actual high-level systems, data pipelines, and tradeoff evaluations.\n"
    "• Code Review & Bug Hunting: Inspecting realistic PRs for concurrency issues, edge cases, and code quality."
)

# Section 2: Elite High-Signal Companies (Top 30 Selection)
h2 = doc.add_paragraph()
h2_run = h2.add_run("2. Top Tier Target Employers (Selection Matrix)")
h2_run.font.name = "Arial"
h2_run.font.size = Pt(14)
h2_run.font.bold = True
h2_run.font.color.rgb = COLOR_PRIMARY

# Table of Top 25 Targets
table = doc.add_table(rows=1, cols=4)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_cells = table.rows[0].cells
headers = ["Company", "Headquarters / Hub", "Evaluation Style", "Target Roles"]
for i, h in enumerate(headers):
    hdr_cells[i].text = h
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="0F172A"/>')
    hdr_cells[i]._tc.get_or_add_tcPr().append(shd)
    for p in hdr_cells[i].paragraphs:
        for r in p.runs:
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            r.font.size = Pt(9)

top_targets = [
    ("Airtable", "San Francisco, CA / Remote", "5-hr realistic design & take-home discussion", "Fullstack / Systems"),
    ("Basecamp / 37signals", "Chicago, IL / Remote", "Take-home project & writing samples", "Backend / Product"),
    ("Zapier", "100% Remote", "Take-home code review & values interview", "Automation / Cloud"),
    ("Adyen", "Amsterdam, NL / Global", "Take-home assignment & design discussion", "Fintech / Payments"),
    ("Automattic", "100% Remote", "Paid trial contract project (2-4 weeks)", "Distributed Systems"),
    ("Docker", "San Francisco, CA / Remote", "Take-home code challenge & pair review", "Infra / Containers"),
    ("GitLab", "100% Remote", "Open source issue pairing & merge request review", "DevOps / Go / Ruby"),
    ("HashiCorp", "San Francisco, CA / Remote", "Take-home architecture & system pairing", "Cloud Infrastructure"),
    ("Mapbox", "Bangalore, IN / SF / Remote", "Conversational review & paid onsite project", "Geospatial / Systems"),
    ("Razorpay", "Bangalore, India", "On-site pair programming on practical tasks", "Fintech / Microservices"),
    ("GoJek", "Bangalore, IN / Jakarta / SG", "Pair programming on real domain challenge", "High-Throughput APIs"),
    ("Zerodha", "Bengaluru, India", "Technical discussion & take-home programming", "Trading Platforms / Go"),
    ("Webflow", "San Francisco, CA / Remote", "Short challenge + paid freelance contract", "Frontend / Canvas UI"),
    ("DuckDuckGo", "100% Remote", "Paid project with current team members", "Search / Privacy"),
    ("Medium", "San Francisco, CA / Remote", "Pairing on real production issues", "Publishing Engine"),
    ("Replit", "San Francisco, CA / Remote", "Pairing on live container/sandbox environment", "Cloud IDE / Compiler"),
    ("Sourcegraph", "Remote", "Practical take-home project + architectural walkthrough", "Developer Tools / Search"),
    ("Vercel", "Remote / Global", "Pair programming on Next.js/React & edge runtimes", "Cloud / Frontend Core")
]

for name, loc, style, role in top_targets:
    row_cells = table.add_row().cells
    row_cells[0].text = name
    row_cells[1].text = loc
    row_cells[2].text = style
    row_cells[3].text = role
    for idx, c in enumerate(row_cells):
        for p in c.paragraphs:
            for r in p.runs:
                r.font.size = Pt(8.5)
                r.font.name = "Calibri"

doc.add_paragraph() # spacer

# Section 3: Take-Home & Pairing Interview Best Practices
h3 = doc.add_paragraph()
h3_run = h3.add_run("3. Candidate Preparation Blueprint")
h3_run.font.name = "Arial"
h3_run.font.size = Pt(14)
h3_run.font.bold = True
h3_run.font.color.rgb = COLOR_PRIMARY

p3 = doc.add_paragraph()
p3.add_run(
    "When applying to non-whiteboard companies, candidates are evaluated on operational hygiene rather than algorithmic memorization:\n\n"
    "1. Git Hygiene & Commit Granularity: Never submit a take-home project with a single 'initial commit'. Create clean, logical commits with clear messages (e.g. feat:, fix:, test:, docs:).\n"
    "2. Production Readability & Tests: Include unit tests (Jest, Vitest, pytest) and defensive error boundary handling. Explain design tradeoffs in a clear README.md.\n"
    "3. Pair Programming Etiquette: Think out loud. Verbalize assumptions, ask clarifying questions on specifications, and treat the interviewer as a collaborative teammate rather than an adversary.\n"
    "4. System Tradeoff Articulation: Be prepared to discuss CAP theorem compromises, caching hierarchies (Redis/CDN), and asynchronous DAG workflows."
)

docx_path = r"e:\anti\reports\HIRING_WITHOUT_WHITEBOARDS_SENIOR_GUIDE.docx"
doc.save(docx_path)
print(f"Generated {docx_path} successfully!")

# Compile to PDF via Word COM
import win32com.client

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
try:
    doc_com = word.Documents.Open(docx_path)
    pdf_path = r"e:\anti\reports\HIRING_WITHOUT_WHITEBOARDS_SENIOR_GUIDE.pdf"
    doc_com.ExportAsFixedFormat(pdf_path, 17) # 17 = wdExportFormatPDF
    page_count = doc_com.ComputeStatistics(2) # 2 = wdStatisticPages
    doc_com.Close(False)
    print(f"Compiled {pdf_path} via Word COM ({page_count} pages) successfully!")
except Exception as e:
    print("[-] Word COM error:", e)
finally:
    word.Quit()
